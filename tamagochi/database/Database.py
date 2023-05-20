from typing import Tuple

import sqlite3

# Should we use Singleton?

class SQLite3Manager:
    def __init__(self, database):
        self.database = database
        self.connection = None

    def getConnection(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.database)

        return self.connection

    def select(self, select_query: str, params: Tuple[str, str] = ()):
        return self.getConnection().cursor().execute(select_query, params).fetchall()

