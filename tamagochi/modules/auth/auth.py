#!/bin/python3

from json import load

import mysql.connector
from argon2 import PasswordHasher

class Auth:
    credentials = load(open('./database.json'))

    database = mysql.connector.connect(
        host=credentials['host'],
        user=credentials['username'],
        password=credentials['password'],
        database=credentials['database']
    )

    def __hashPassword(self, password: str) -> str:
        ph = PasswordHasher()
        return ph.hash(password)

    def login(self, user: str, password: str) -> bool:
        cursor = self.database.cursor()
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()

        for row in result:
            print(row)

        return True

