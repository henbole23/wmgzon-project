import sqlite3



class Database():
    def __init__(self, db_name):
        self.db = db_name

    def connect(self):
        try:
            db = sqlite3.connect(self.db)
        except Error as e:
            print(e)