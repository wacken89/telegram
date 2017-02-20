#!/bin/bash
echo "Creating file with variables"
j2 vars.py.j2 > vars.py

echo
echo "Starting Telegram Bot"
echo
python bot.py