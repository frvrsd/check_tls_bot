#!/usr/bin/python3
import ssl
import socket
from datetime import datetime
import asyncio
import logging
from telegram import Bot
from telegram.error import RetryAfter
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import subprocess

subprocess.run(["/usr/bin/python3", "/projects/Python/cert_check/bin/sort.py"])

with open("/projects/Python/cert_check/logs/certs_bot.log", "w"):
    pass

logging.basicConfig(
    filename="/projects/Python/cert_check/logs/certs_bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    encoding="utf-8",
)

telegram_bot_token = "Y"
chat_id = "" #your chat id with bot (you can send command /chatid when button.py started)


async def get_certificate_expiry_date(hostname):
    try:
        context = ssl._create_unverified_context()  # Создаем непроверенный контекст SSL
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                cert_bin = sslsock.getpeercert(True)
                cert = x509.load_der_x509_certificate(cert_bin, default_backend())
                # logging.info(f'Сертификат для {hostname}: {cert}')
                not_after = cert.not_valid_after
                expiry_date = not_after.replace(tzinfo=None)
                logging.info(f'Сертификат для {hostname} истекает {expiry_date}')
                return expiry_date
    except ssl.SSLError as e:
        logging.error(f'Ошибка при проверке сертификата на {hostname}, {e}')
        return None
    except socket.gaierror as e:
        logging.error(f'Ошибка при разрешении имени хоста {hostname}: {e}')
        return None


async def send_notification(bot, message):
    try:
        logging.info(f"Отправляем сообщение: {message}")
        await bot.send_message(chat_id=chat_id, text=message)
        logging.info("Сообщение успешно отправлено!")
    except RetryAfter as e:
        logging.warning(
            f"Превышено ограничение на отправку. Повторная попытка через {e.retry_after} секунд."
        )
        await asyncio.sleep(e.retry_after)
        await send_notification(bot, message)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


def plural_days(days, one_day="день", two_days="дня", five_days="дней"):
    # Склонение слова 'день' в зависимости от числа дней
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} {one_day}"
    elif days % 10 in (2, 3, 4) and days % 100 not in (12, 13, 14):
        return f"{days} {two_days}"
    else:
        return f"{days} {five_days}"


async def check_certificates_batch(bot, batch):
    today = datetime.now()
    for hostname, website_name in batch:
        expiry_date = await get_certificate_expiry_date(hostname)
        if expiry_date:
            days_until_expiry = (expiry_date - today).days
            if days_until_expiry <= -1:
                message = f"🚨🚨🚨CRITICAL \n Сертификат для {website_name} ({hostname}) просрочен на {plural_days(-days_until_expiry)}! 🚨🚨🚨"
                await send_notification(bot, message)
            elif days_until_expiry <= 3:
                message = f"🚨CRITICAL \n Сертификат для {website_name} ({hostname}) истекает через {plural_days(days_until_expiry)}! 🚨"
                await send_notification(bot, message)
            elif days_until_expiry <= 10:
                message = f"🟡WARNING \n Сертификат для {website_name} ({hostname}) истекает через {plural_days(days_until_expiry)}! 🟡"
                await send_notification(bot, message)



async def check_certificates(bot):
    try:
        logging.info("Начинаем проверку сертификатов...")
        with open("/projects/Python/cert_check/config/sites.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        batch_size = 2  # Размер пакета
        for i in range(0, len(lines), batch_size):
            batch = []
            for line in lines[i : i + batch_size]:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                parts = line.split("#")
                if len(parts) >= 2:
                    hostname = parts[0].strip()
                    website_name = parts[1].strip()
                    batch.append((hostname, website_name))
            if batch:
                await check_certificates_batch(bot, batch)

        logging.info("Проверка завершена.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


async def main():
    bot = Bot(token=telegram_bot_token)
    while True:
        await check_certificates(bot)
        await asyncio.sleep(86400)



if __name__ == "__main__":
    asyncio.run(main())
