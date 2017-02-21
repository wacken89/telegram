#!/bin/bash

echo "Checking mysql status"
while [[ "`cat /status/db.status`" == '0' ]];do 
	echo "Database doesn't ready. Waiting 10 seconds"
	sleep 10
done

echo "Creating file with variables"
j2 vars.py.j2 > vars.py

echo
echo "Starting Telegram Checker"
echo
python checker.py