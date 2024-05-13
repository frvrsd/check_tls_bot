#!/usr/bin/python3
from datetime import datetime

with open("/projects/Python/cert_check/logs/certs_bot.log", "r", encoding="utf-8") as log_file: #your path to logs
    log_lines = log_file.readlines()

log_with_dates = []
for line in log_lines:
    parts = line.split(" - ")
    if len(parts) >= 3:
        cert_info = parts[-1]
        cert_date_str = cert_info.split(" истекает ")[-1].strip()
        site_name = cert_info.split(" для ")[-1].split(" истекает ")[0].strip()
        try:
            cert_date = datetime.strptime(cert_date_str, "%Y-%m-%d %H:%M:%S")
            log_with_dates.append((cert_date, site_name))
        except ValueError:
            pass

log_with_dates.sort(key=lambda x: x[0])

with open("/projects/Python/cert_check/logs/certs_bot_sorted.log", "w", encoding="utf-8") as sorted_log_file: #your path to logs
    for line in log_with_dates:
        sorted_log_file.write(f"{line[1]} истекает {line[0].strftime('%Y-%m-%d %H:%M:%S')}\n")
