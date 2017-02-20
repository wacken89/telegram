# -*- coding: utf-8 -*-

import telebot
import vars
import sys
import datetime
import MySQLdb

bot = telebot.TeleBot(vars.token)

print(bot.get_me())
db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
cursor = db.cursor()

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
  user_markup.row('/help', '/join')
  user_markup.row('/listusers', '/blockuser', '/turnon', '/turnoff')
  user_markup.row('Hello', 'Bye')
  bot.send_message(message.from_user.id, "welcome..", reply_markup=user_markup)

@bot.message_handler(commands=['help'])
def handle_start(message):
  bot.send_message(message.chat.id, "usage:\n\tPrint [hello]\n\tPrint [bye]")

@bot.message_handler(commands=['join'])
def handle_start(message):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  sql = "INSERT INTO users(telegram_id, username, blocked, show_pics) VALUES ('%s', '%s' , 1, 1)" % (message.from_user.id ,message.from_user.first_name + " " + message.from_user.last_name)
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
     bot.send_message(message.chat.id, "Everething GOOD" + " " + message.from_user.first_name )
  except:
     # Rollback in case there is any error
     db.rollback()
     bot.send_message(message.chat.id, "Everething BAD" + " " + message.from_user.first_name )

  # disconnect from server
  db.close()

@bot.message_handler(commands=['listusers'])
def handle_start(message):
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
      answer = "ID in Database:  %s\nTelegram ID:  %s\nName:  %s\nBlocked user:  %s\nShow pictures: %s\n" % (id, telegram_id, username, blocked, show_pics )
      bot.send_message(message.chat.id, answer)
  except:
     print "Error: unable to fecth data"
     bot.send_message(message.chat.id, "Error: unable to fecth data")
  db.close()


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