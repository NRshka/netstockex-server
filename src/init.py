import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE users 
                    (login text, email text, password text, 
                    last_login text, bot_token text)""")
