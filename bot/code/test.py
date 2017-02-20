# -*- coding: utf-8 -*-

import vars
import MySQLdb

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
      print "id=%s,telegram_id=%s,username=%s,blocked=%s,show_pics=%s" % \
             (id, telegram_id, username, blocked, sh )
except:
   print "Error: unable to fecth data"


# disconnect from server
db.close()