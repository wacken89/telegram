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
  print(row_count)
  db.close()
  return row_count


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
  user_markup.row('/start', '/stop', '/join', '/help')
  user_markup.row('/Notificaton on', '/Notificaton off')
  user_markup.row('/listusers', '/blockuser', '/deleteuser')
  bot.send_message(message.from_user.id, "welcome..", reply_markup=user_markup)

@bot.message_handler(commands=['help'])
def handle_help(message):
  bot.send_message(message.chat.id, "usage:\n\tPrint [hello]\n\tPrint [bye]")

@bot.message_handler(commands=['join'])
def handle_join(message):
  if checkUser(message.from_user.id) == 1:
    bot.send_message(message.chat.id, message.from_user.first_name + " " +  "you've already in database" )
  else:
    db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
    cursor = db.cursor()
    sql = "INSERT INTO users(telegram_id, username, blocked, show_pics) VALUES ('%s', '%s' , 1, 1)" % (message.from_user.id ,message.from_user.first_name + " " + message.from_user.last_name)
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

@bot.message_handler(commands=['listusers'])
def handle_listusers(message):
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
      blocked = row[3]
      show_pics = row[4]
      # Now print fetched result
      if (blocked == 1) : 
        blocked_print = 'yes'
      else:
        blocked_print = 'no'
      if (show_pics == 1):
        show_pics_print = 'yes'
      else:
        show_pics_print = 'no'
      answer = "ID in Database:  %s\nTelegram ID:  %s\nName:  %s\nBlocked user:  %s\nShow pictures: %s\n" % (id, telegram_id, username, blocked_print, show_pics_print )
      bot.send_message(message.chat.id, answer)
  except:
     print "Error: unable to fecth data"
     bot.send_message(message.chat.id, "Error: unable to fecth data")
  db.close()

@bot.message_handler(commands=['blockuser'])
def handle_blockuser(message):
  bot.send_message(message.chat.id, "Blockuser section")

@bot.message_handler(content_types=['text'])
def handle_text(message):
  answer = "I don't understand"
  if message.text == "Hello" or message.text == "hello":
    answer = "Hello " + message.from_user.first_name
    log(message, answer)
    bot.send_message(message.chat.id, answer)
  elif message.text == "bye" or message.text == "Bye":
  	bot.send_message(message.chat.id, "Good bye")
  else:
    log(message, answer)
    bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)