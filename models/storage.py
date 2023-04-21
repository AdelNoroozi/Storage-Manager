import sqlite3


class StorageModel:
    def __init__(self, name, is_available):
        self.name = name
        self.is_available = is_available

    def json(self):
        return {'name': self.name, 'is_available': self.is_available}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('./dbsqlite3.db')
        cursor = connection.cursor()
        query = "SELECT * FROM storages WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('./dbsqlite3.db')
        cursor = connection.cursor()
        query = "INSERT INTO storages VALUES (?, ?)"
        cursor.execute(query, (self.name, self.is_available))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('./dbsqlite3.db')
        cursor = connection.cursor()
        query = "UPDATE storages SET is_available=? WHERE name=?"
        cursor.execute(query, (self.is_available, self.name))
        connection.commit()
        connection.close()
