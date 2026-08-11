import sqlite3


class DatabaseManager:

    def __init__(self):

        self.connection = sqlite3.connect("database/reports.db")

        self.connection.execute("PRAGMA foreign_keys = ON")

        self.connection.row_factory = sqlite3.Row
        
        self.cursor = self.connection.cursor()

    def get_connection(self):

        return self.connection

    def commit(self):

        self.connection.commit()

    def close(self):

        self.connection.close()