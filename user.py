import json
import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="missing field: username")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="missing field: password")

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        username = data['username']
        if User.find_by_username(username):
            return {'message': "username already exists"}
        else:
            password = data['password']
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cursor.execute(query, (username, password))
            connection.commit()
            connection.close()
            user = User.find_by_username(username)
            user_json = {"id": user.id,
                         "username": user.username}
            return user_json, 201
