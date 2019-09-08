from .logining import *
import sqlite3
import os

#иницилизируем базу данных
if not os.path.exists('users.db'):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE users 
                    (login text, email text, password text, 
                    last_login text, bot_token text)""")