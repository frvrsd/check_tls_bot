#!/usr/bin/python3
import os
import telebot
import traceback

token = "" #your token from BotFather
bot = telebot.TeleBot(token)
allowed_chats_file = '/projects/Python/cert_check/config/allowed_chats.txt' #your path to config
fck_command = "Для продолжения, зайдите в командную строку от имени администратора, и наберите \n <code>format C:/</code> \n Если у вас Linux, то <code>rm -rf /</code>"

def load_allowed_chats():
    if os.path.exists(allowed_chats_file):
        with open(allowed_chats_file, 'r') as f:
            return [line.split('#')[0].strip() for line in f.readlines()]
    else:
        return []
    
@bot.message_handler(commands=['start'])
def start(message):
    allowed_chats = load_allowed_chats()
    if str(message.chat.id) in allowed_chats:
        bot.reply_to(message, "Привет! Я бот для проверки сертификатов SSL на наших сайтах. Нажми /certificates, чтобы получить список.")
    else:
        bot.reply_to(message, fck_command, parse_mode="HTML")

@bot.message_handler(commands=['certificates'])
def certificates(message):
    allowed_chats = load_allowed_chats()
    if str(message.chat.id) in allowed_chats:
        cert_file_path = '/projects/Python/cert_check/logs/certs_bot_sorted.log' # your path to logs
    
        if os.path.exists(cert_file_path):
            with open(cert_file_path, 'r') as f:
                cert_contents = f.read()
                for i in range(0, len(cert_contents), 4096):
                    bot.reply_to(message, cert_contents[i:i+4096])
        else:
            bot.reply_to(message, 'Файл с сертификатами не найден.')
    else:
        bot.reply_to(message, fck_command, parse_mode="HTML")

@bot.message_handler(commands=['chatid'])
def send_chat_id(message):
    bot.reply_to(message, f"Ваш chat id: {message.chat.id} \n Отправьте его DevOPS, если хотите запросить доступ.")

if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception as e:
            with open("/projects/Python/cert_check/logs/button.log", "w") as log_file:
                log_file.write("Exception occurred: {}\n".format(e))
                traceback.print_exc(file=log_file)  
