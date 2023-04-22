# import sqlite3

from db import db


class StorageModel(db.Model):
    __tablename__ = 'storages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    is_available = db.Column(db.String(10))

    def __init__(self, name, is_available):
        self.name = name
        self.is_available = is_available

    def json(self):
        return {'name': self.name, 'is_available': self.is_available}

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect('./dbsqlite3.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM storages WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row)
        return cls.query.filter_by(name=name).first()

    def save(self):
        # connection = sqlite3.connect('./dbsqlite3.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO storages VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.is_available))
        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()

    # def update(self):
    #     connection = sqlite3.connect('./dbsqlite3.db')
    #     cursor = connection.cursor()
    #     query = "UPDATE storages SET is_available=? WHERE name=?"
    #     cursor.execute(query, (self.is_available, self.name))
    #     connection.commit()
    #     connection.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
