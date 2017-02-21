# -*- coding: utf-8 -*-

import telebot
import vars
import sys
import datetime
import MySQLdb

bot = telebot.TeleBot(vars.token)

print(bot.get_me())