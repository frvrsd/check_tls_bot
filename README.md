# Check TLS Bot

This is a Telegram bot written in Python that checks SSL certificates for all websites from a list and provides a sorted list of all websites with their certificate expiration dates upon request.

## Running the Bot

To run the Telegram bot, you need to execute the `button.py` script. This script initializes the bot and provides commands for interacting with it.

Ensure that you have the necessary dependencies installed, such as `telebot` and `telegram`. You can install them via pip:

pip install pyTelegramBotAPI
pip install python-telegram-bot


Before running the bot, make sure to configure the necessary paths and settings in the code, such as the bot token, allowed chat IDs, and file paths.

### Running as a System Service (Systemd)

You can also run the bot as a systemd service to ensure it starts automatically and restarts in case of failure. Here's an example systemd unit file:

<code>[Unit]
Description=Check TLS Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/your/project/directory
ExecStart=/usr/bin/python3 /path/to/your/project/directory/button.py
Restart=always

[Install]
WantedBy=multi-user.target</code>

Replace `your_username` with your username and `/path/to/your/project/directory` with the path to your project directory.

Save this file as `check_tls_bot.service` in `/etc/systemd/system/` directory and activate it using the following commands:

sudo systemctl daemon-reload
sudo systemctl enable check_tls_bot.service
sudo systemctl start check_tls_bot.service


Now your bot will start automatically upon system boot and restart in case of any failure.

Feel free to modify the code according to your requirements and extend its functionality as needed.
