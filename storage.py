from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
import sqlite3


class Storage(Resource):
    storage_parser = reqparse.RequestParser()
    storage_parser.add_argument('is_available',
                                type=str,
                                required=True,
                                help="missing field: is_available")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        query = "SELECT * FROM storages WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {
                'name': row[0],
                'is_available': row[1]
            }}, 200

    def get(self, name):
        storage = Storage.find_by_name(name=name)
        if storage:
            return storage
        else:
            return {'message': "storage not found"}, 404

    @classmethod
    def insert(cls, storage):
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        query = "INSERT INTO storages VALUES (?, ?)"
        cursor.execute(query, (storage['name'], storage['is_available']))
        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if Storage.find_by_name(name=name):
            return {'message': f"storage with name {name} already exists"}, 400
        data = Storage.storage_parser.parse_args()  # by using 'force = True' we can bypass content type header in our request, however it,s dangerous, and it is only useful for easier testing
        storage = {'name': name, 'is_available': data['is_available']}
        try:
            Storage.insert(storage=storage)
        except:
            return {'message': "something went wrong"}, 500
        return storage, 201

    @jwt_required()
    def delete(self, name):
        if not Storage.find_by_name(name):
            return {'message': "storage not found"}, 404
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        query = "DELETE FROM storages WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "storage deleted successfully"}, 200

    @classmethod
    def update(cls, storage):
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        query = "UPDATE storages SET is_available=? WHERE name=?"
        cursor.execute(query, (storage['is_available'], storage['name']))
        connection.commit()
        connection.close()

    @jwt_required()
    def put(self, name):
        data = Storage.storage_parser.parse_args()
        storage = Storage.find_by_name(name)
        patched_storage = {'name': name, 'is_available': data['is_available']}
        if storage is None:
            try:
                Storage.insert(storage=patched_storage)
            except:
                return {'message': "something went wrong"}, 500
        else:
            try:
                Storage.update(storage=patched_storage)
            except:
                return {'message': "something went wrong"}, 500
        return patched_storage, 200


class StorageList(Resource):
    def get(self):
        connection = sqlite3.connect('dbsqlite3.db')
        cursor = connection.cursor()
        query = "SELECT * FROM storages"
        result = cursor.execute(query)
        storages = []
        for row in result:
            storages.append(
                {
                    'name': row[0],
                    'is_available': row[1]
                }
            )
        connection.close()
        return {'storages': storages}
