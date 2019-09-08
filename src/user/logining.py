'''
Модуль, который отвечает заработу с данными пользователя,
не относящиеся к игровому процессу напрямую. Содержит функции
логина, авторизации, регистрации, хранения данных и т.п.
Пока использую sqlite3, потом что-то эффективнее.

@author ADT
'''

import sqlite3 as sql3
import hashlib
import datetime


conn = sql3.connect('users.db')
cursor = conn.cursor()
hasher = hashlib.sha512()


def login(username: str, pass_hash: str) -> bool:
    request = 'SELECT * FROM users WHERE login=? AND password=?'
    cursor.execute(request, (username, pass_hash))

    if cursor.fetchone() is None:
        return False

    time = datetime.datetime.today().strftime("%d-%m-%Y %H:%M:%S")
    request = 'UPDATE users SET last_login=? WHERE login=?'
    cursor.execute(request, (time, username))
    conn.commit()

    return True



def register(username: str, email: str, pass_hash: str) -> True:
    request = "SELECT * FROM users WHERE email=? OR login=?"
    cursor.execute(request, (email, username))

    if cursor.fetchone():
        return False

    request = 'INSERT INTO users VALUES (?, ?, ?, ?, ?)'
    cursor.execute(request, (username, email, pass_hash, 'None', 'None'))
    conn.commit()

    return True