#!/bin/bash -xue
# Create virtual env
python3 -m venv env

# Activate virtual env
source env/bin/activate

# Install packages in virtual env
# pip3 install python-telegram-bot --upgrade
# pip3 install pyTelegramBotAPI
# pip3 install -U googlemaps
# pip3 install geopy
# pip3 install prettyprint

# Run python file in virtual env
python3 telegram_bot.py