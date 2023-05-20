from typing import Tuple

import sqlite3

# Should we use Singleton?

class SQLite3Manager:
    def __init__(self, database):
        self.database = database
        self.connection = None

    def getConnection(self):
        if not self.connection or self._isClosed(self.connection):
            self.connection = sqlite3.connect(self.database)

        return self.connection
    
    def _isClosed(self, conn: sqlite3.Connection) -> bool:
        try:
            conn.execute('')
        except sqlite3.ProgrammingError:
            return True
        
        return False
    
    def query(self, sql: str, params: Tuple[str, str] = (), type: str = "select"):
        """
        Query the database. 
        Arguments:
         sql: SQL statement, such as 'SELECT email, password FROM Users WHERE id = ?'
         params: tuple of parameters to be inserted in the sql 
         type: type of the operation ("select", "change")
        """

        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute(sql, params) 
        
        if type == "select":
            result = cursor.fetchall()

        if type == "change":
            result = []
            conn.commit()

        cursor.close()
        conn.close()
        return result


