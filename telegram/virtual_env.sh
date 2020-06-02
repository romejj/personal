#!/bin/bash -xue
# Create virtual env
python3 -m venv env

# Activate virtual env
source env/bin/activate

# Install packages in virtual env
# pip3 install -r requirements.txt

# Run python file in virtual env
python3 telegram_bot.py