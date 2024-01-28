import sqlite3



class Database():
    def __init__(self, db_name):
        self.databse = db_name

    def connect(self):
        try:
            db = sqlite3.connect(self.database)
        except Error as e:
            print(e)