#!/bin/bash -xue
# Argument check
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
fi

g_api_key=$1
t_token=$2
tmdb_api_key=$3

# Create virtual env
python3 -m venv env

# Activate virtual env
source env/bin/activate

# Install packages in virtual env
# pip3 install -r requirements.txt

# Run python file in virtual env in background
nohup python3 telegram_bot.py $g_api_key $t_token $tmdb_api_key