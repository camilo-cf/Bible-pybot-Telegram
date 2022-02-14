'''
    Send the daily chapter to the group of registered/ subscribed users
    This will be used as a daily crontab task
'''
import main
import Database_control

connection, cursor = Database_control.create_db()
response = Database_control.get_subscribed_user(cursor)
Database_control.close_db(connection)

for each_id in response:
    main.command_send_chapter_crontab(each_id[0])
