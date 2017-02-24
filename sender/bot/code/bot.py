# -*- coding: utf-8 -*-

import telebot
import vars
import sys
import datetime
import MySQLdb

bot = telebot.TeleBot(vars.token)
print(bot.get_me())


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

def notificationCheck(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  cursor.execute("SELECT notifications  FROM users WHERE telegram_id = %s" % (telegramid))
  return cursor.fetchone()[0]
  db.close()

def notificationModify(action, telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  sql = "UPDATE users SET notifications ='%s' WHERE telegram_id='%s'" % (action, telegramid)
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
  except:
     # Rollback in case there is any error
     db.rollback()
  

def log(message, answer):
  sys.stderr.write("\n-------------")
  from datetime import datetime
  print(datetime.now())
  sys.stderr.write("Message from {0} {1}. (id = {2}) \n Text - {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id),
                                                                message.text))
  sys.stderr.write(answer)

@bot.message_handler(commands=['start'])
def handle_start(message):
  user_markup = telebot.types.ReplyKeyboardMarkup(True)
  user_markup.row('/start', '/join', '/help')
  user_markup.row('/notificaton_on', '/notificaton_off')
  if checkUser(message.from_user.id) >= 1:
    if adminCheck(message.from_user.id) == 1:
      user_markup.row('/listusers')
  bot.send_message(message.from_user.id, "welcome..", reply_markup=user_markup)

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
      sql = "INSERT INTO users(telegram_id, username, active, notifications, admin) VALUES ('%s', '%s' , 1, 1, 0)" % (message.from_user.id ,message.from_user.first_name + " " + message.from_user.last_name)
    else:
      sql = "INSERT INTO users(telegram_id, username, active, notifications, admin) VALUES ('%s', '%s' , 1, 1, 0)" % (message.from_user.id ,message.from_user.first_name)
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
  if checkUser(message.from_user.id) >= 1:
    if notificationCheck(message.from_user.id) == 1:
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are receiving messages")
    elif notificationCheck(message.from_user.id) == 0:
      notificationModify(1, message.from_user.id)
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are start receiving messages")
    else:
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are not in database. Please join us click on /join" )

@bot.message_handler(commands=['notificaton_off'])
def handle_listusers(message):
  if checkUser(message.from_user.id) >= 1:
    if notificationCheck(message.from_user.id) == 0:
      bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you are not receiving messages")
    elif notificationCheck(message.from_user.id) == 1:
      notificationModify(0, message.from_user.id)
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
        keyboard = telebot.types.InlineKeyboardMarkup()
        callback_button = telebot.types.InlineKeyboardButton(text="Block" , callback_data="test")
        callback_button1 = telebot.types.InlineKeyboardButton(text="Delete", callback_data="test")
        callback_button2 = telebot.types.InlineKeyboardButton(text="Grant Admin privileges" , callback_data="admin")
        keyboard.add(callback_button, callback_button1)
        keyboard.add(callback_button2)
        bot.send_message(message.chat.id, answer, reply_markup=keyboard)
    except:
       print "Error: unable to fecth data"
       bot.send_message(message.chat.id, "Error: unable to fecth data")
    db.close()
  else:
    bot.send_message(message.chat.id, "You are not allowed execute this command")


@bot.message_handler(commands=['blockuser'])
def handle_blockuser(message):
  bot.send_message(message.chat.id, "Blockuser section")

@bot.message_handler(content_types=['text'])
def handle_text(message):
  answer = "I don't understand"
  if message.text == "Hello" or message.text == "hello":
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button = telebot.types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)
  elif message.text == "bye" or message.text == "Bye":
    bot.send_message(message.chat.id, "Good bye")
  elif message.text == "test" or message.text == "test":
    bot.send_message(message.chat.id, "TEST ME")
  else:
    bot.send_message(message.chat.id, answer)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.send_message(call.message.chat.id, "HELLO")

bot.polling(none_stop=True, interval=0)