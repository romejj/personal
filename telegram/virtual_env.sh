#!/bin/bash -xue
# Argument check
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
fi

g_api_key=$1
t_token=$2

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

# Run python file in virtual env in background
nohup python3 telegram_bot.py $g_api_key $t_token

# Kill process
# pkill -f telegram_bot.py