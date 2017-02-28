# -*- coding: utf-8 -*-

import telebot
from telebot import types
import vars
import sys
import datetime
import MySQLdb

bot = telebot.TeleBot(vars.token)
print(bot.get_me())
user_dict = {}

def checkUser(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  cursor.execute("SELECT id, COUNT(*) FROM users WHERE telegram_id = %s GROUP BY id" % (telegramid))
  row_count = cursor.rowcount
  db.close()
  return row_count

def adminCheck(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  cursor.execute("SELECT admin FROM users WHERE telegram_id = %s" % (telegramid))
  return cursor.fetchone()[0]
  db.close()

def enableCheck(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  cursor.execute("SELECT active FROM users WHERE telegram_id = %s" % (telegramid))
  return cursor.fetchone()[0]
  db.close()

def notificationCheck(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  cursor.execute("SELECT notifications  FROM users WHERE telegram_id = %s" % (telegramid))
  return cursor.fetchone()[0]
  db.close()

def entryModify(column ,action, telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  sql = "UPDATE users SET %s ='%s' WHERE telegram_id='%s'" % (column, action, telegramid)
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
  except:
     # Rollback in case there is any error
     db.rollback()
  db.close()

def deleteUser(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  sql = "DELETE FROM users WHERE telegram_id = '%s'" % (telegramid)
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
  except:
     # Rollback in case there is any error
     db.rollback()
  db.close()

def log(message, answer):
  sys.stderr.write("\n-------------")
  from datetime import datetime
  print(datetime.now())
  sys.stderr.write("Message from {0} {1}. (id = {2}) \n Text - {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id),
                                                                message.text))
  sys.stderr.write(answer)

@bot.message_handler(commands=['start', 'refresh'])
def handle_start(message):
  user_markup = telebot.types.ReplyKeyboardMarkup(True)
  user_markup.row('/join', '/help', '/refresh')
  user_markup.row('/notificaton_on', '/notificaton_off')
  if checkUser(message.from_user.id) >= 1:
    if adminCheck(message.from_user.id) == 1:
      user_markup.row('/listusers', '/modifiy')
  bot.send_message(message.from_user.id, "Let's start ...", reply_markup=user_markup)

@bot.message_handler(commands=['help'])
def handle_help(message):
  bot.send_message(message.chat.id, "usage:\n\tPrint [hello]\n\tPrint [bye]")

@bot.message_handler(commands=['join'])
def handle_join(message):
  if checkUser(message.from_user.id) >= 1:
    bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you've already in database" )
  else:
    db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
    cursor = db.cursor()
    if message.from_user.last_name:
      fullName = message.from_user.first_name + " " + message.from_user.last_name
    else:
      fullName = message.from_user.first_name
    sql = "INSERT INTO users(telegram_id, username, active, notifications, admin) VALUES ('%s', '%s' , 0, 0, 0)" % (message.from_user.id , fullName)
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
       bot.send_message(message.chat.id, message.from_user.first_name + " " +  "was added to database" )
    except:
       # Rollback in case there is any error
       db.rollback()
       bot.send_message(message.chat.id,  message.from_user.first_name + " " + "wasn't added to database. Please ask administrator" )

    # disconnect from server
    db.close()

@bot.message_handler(commands=['notificaton_on'])
def handle_listusers(message):
  column = 'notifications'
  if checkUser(message.from_user.id) >= 1:
    if notificationCheck(message.from_user.id) == 1:
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are receiving messages")
    elif notificationCheck(message.from_user.id) == 0:
      entryModify(column, 1, message.from_user.id)
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are start receiving messages")
    else:
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are not in database. Please join us click on /join" )

@bot.message_handler(commands=['notificaton_off'])
def handle_listusers(message):
  column = 'notifications'
  if checkUser(message.from_user.id) >= 1:
    if notificationCheck(message.from_user.id) == 0:
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are not receiving messages")
    elif notificationCheck(message.from_user.id) == 1:
      entryModify(column, 0, message.from_user.id)
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are stop receiving messages")
  else:
    bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are not in database. Please join us click on /join" )


@bot.message_handler(commands=['listusers'])
def handle_listusers(message):
  if adminCheck(message.from_user.id) == 1:
    db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
    cursor = db.cursor()
    sql = "SELECT * FROM users;"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       for row in results:
        id = row[0]
        telegram_id = row[1]
        username = row[2]
        active = row[3]
        notifications = row[4]
        admin = row[5]
        # Now print fetched result
        if (active == 1) : 
          active_print = 'enabled'
        else:
          active_print = 'disabled'
        if (notifications == 1):
          notifications_print = 'yes'
        else:
          notifications_print = 'no'
        if (admin == 1):
          admin_print = 'admin'
        else:
          admin_print = 'user'
        answer = "ID in Database:  %s\nTelegram ID:  %s\nName:  %s\nUser status:  %s\nAdmin status: %s\nReceive messages: %s\n" % (id, telegram_id, username, active_print, admin_print, notifications_print )
        bot.send_message(message.chat.id, answer)
    except:
       print "Error: unable to fecth data"
       bot.send_message(message.chat.id, "Error: unable to fecth data")
    db.close()

class User:
    def __init__(self, name):
        self.name = name
        self.telegramID = None
        self.action = None

@bot.message_handler(commands=['modifiy'])
def process_name_step(message):
  if adminCheck(message.from_user.id) == 1:
      try:
          chat_id = message.chat.id
          name = message.text
          user = User(name)
          user_dict[chat_id] = user
          msg = bot.reply_to(message, 'Enter user id. You can get it from /listusers')
          bot.register_next_step_handler(msg, process_age_step)
      except Exception as e:
          bot.reply_to(message, 'Error')
  else:
    bot.send_message(message.chat.id, "You are not allowed execute this command")


def process_age_step(message):
  try:
      chat_id = message.chat.id
      telegramID = message.text
      if not telegramID.isdigit():
          msg = bot.reply_to(message, 'ID should be a number')
          bot.register_next_step_handler(msg, process_age_step)
          return
      user = user_dict[chat_id]
      user.telegramID = telegramID
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
      markup.add('Enable/Disable', 'Delete')
      msg = bot.reply_to(message, 'What action you want do?', reply_markup=markup)
      bot.register_next_step_handler(msg, process_action_step)
  except Exception as e:
      bot.reply_to(message, 'Error')


def process_action_step(message):
  try:
      chat_id = message.chat.id
      action = message.text
      user = user_dict[chat_id]
      if (action == u'Enable/Disable'):
        column = 'active'
        user.action = action
        if checkUser(str(user.telegramID)) >= 1:
          if enableCheck(str(user.telegramID)) == 1:
            entryModify(column, 0, str(user.telegramID))
            bot.send_message(chat_id, 'Telegram ID:' + " " + str(user.telegramID) + " " + 'enabled. Disabling .... ')
            handle_start(message)
          elif enableCheck(str(user.telegramID)) == 0:
            entryModify(column, 1, str(user.telegramID))
            bot.send_message(chat_id, 'Telegram ID:' + " " + str(user.telegramID) + " " + 'disabled. Enabling .... ')
            handle_start(message)
        else:
          bot.send_message(chat_id, 'Telegram ID:' + " " + str(user.telegramID) + " " + 'not in database')
          handle_start(message)
      elif (action == u'Delete'):
        if checkUser(str(user.telegramID)) >= 1:
          deleteUser(str(user.telegramID))
          bot.send_message(chat_id, 'Telegram ID:' + " " + str(user.telegramID) + " " + 'Deleted.')
          handle_start(message)
        else:
          bot.send_message(chat_id, 'Telegram ID:' + " " + str(user.telegramID) + " " + 'not in database')
          handle_start(message)
      else:
          raise Exception()
  except Exception as e:
      bot.reply_to(message, 'NOT OK')

bot.polling(none_stop=True, interval=0)