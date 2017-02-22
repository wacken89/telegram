import time
import vars
import sys
import telebot
import MySQLdb
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler  

bot = telebot.TeleBot(vars.token)

class MyHandler(PatternMatchingEventHandler):
  patterns = ["*.jpg", "*.png"]

  def checkUser(telegramid):
   db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
   cursor = db.cursor()
   cursor.execute("SELECT id, COUNT(*) FROM users WHERE telegram_id = %s GROUP BY id" % (telegramid))
   row_count = cursor.rowcount
   db.close()
   return row_count

  def process(self, event):
    event.event_type 
    event.is_directory
    event.src_path
    return event.src_path

  def on_created(self, event):
        self.process(event)
        db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
        cursor = db.cursor()
        sql = "SELECT telegram_id FROM observe.users WHERE active = 1 AND notifications = 1 ;"
        try:
          # Execute the SQL command
          cursor.execute(sql)
          # Fetch all the rows in a list of lists.
          results = cursor.fetchall()
          for row in results:
            telegram_id = row[0]
            img = open(event.src_path, 'rb')
            bot.send_chat_action(telegram_id, 'upload_photo')
            bot.send_photo(telegram_id, img)
            img.close()
        except:
          print "Error: unable to fecth data"
          bot.send_message(telegram_id, "Error: unable to fecth data")
        db.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()