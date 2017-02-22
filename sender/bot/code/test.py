# -*- coding: utf-8 -*-

import vars
import MySQLdb

def checkUser(action, telegramid):
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