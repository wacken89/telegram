# -*- coding: utf-8 -*-

import vars
import MySQLdb

def notification_check(telegramid):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()

def notification(telegramid, value):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  cursor.execute("SELECT id, COUNT(*) FROM users WHERE telegram_id = %s GROUP BY id" % (telegramid))
  row_count = cursor.rowcount
  print(row_count)
  db.close()
  return row_count

telegramid = 1
if checkUser(telegramid) == 1:
  print 'exists'
else
  print "non exists"