import json
import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


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
        # connection = sqlite3.connect('./dbsqlite3.db')
        # cursor = connection.cursor()
        username = data['username']
        if UserModel.find_by_username(username):
            return {'message': "username already exists"}, 400
        password = data['password']
        if len(password) < 8:
            return {'message': "password is too short"}, 400
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (username, password))
        # connection.commit()
        # connection.close()
        user_obj = UserModel(username=username, password=password)
        user_obj.save(lo=4)
        user_json = {"username": user_obj.username}
        return user_json, 201
