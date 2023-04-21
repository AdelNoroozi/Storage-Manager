from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
import sqlite3

from models.storage import StorageModel


class Storage(Resource):
    storage_parser = reqparse.RequestParser()
    storage_parser.add_argument('is_available',
                                type=str,
                                required=True,
                                help="missing field: is_available")

    def get(self, name):
        storage = StorageModel.find_by_name(name=name)
        if storage:
            return storage.json()
        else:
            return {'message': "storage not found"}, 404

    @jwt_required()
    def post(self, name):
        if StorageModel.find_by_name(name=name):
            return {'message': f"storage with name {name} already exists"}, 400
        data = Storage.storage_parser.parse_args()  # by using 'force = True' we can bypass content type header in our request, however it,s dangerous, and it is only useful for easier testing
        is_available = data['is_available']
        storage = StorageModel(name, is_available)
        try:
            storage.insert()
        except:
            return {'message': "something went wrong"}, 500
        return storage.json(), 201

    @jwt_required()
    def delete(self, name):
        if not StorageModel.find_by_name(name):
            return {'message': "storage not found"}, 404
        connection = sqlite3.connect('./dbsqlite3.db')
        cursor = connection.cursor()
        query = "DELETE FROM storages WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "storage deleted successfully"}, 200

    @jwt_required()
    def put(self, name):
        data = Storage.storage_parser.parse_args()
        storage = StorageModel.find_by_name(name)
        is_available = data['is_available']
        patched_storage = StorageModel(name=name, is_available=is_available)
        if storage is None:
            try:
                patched_storage.insert()
            except:
                return {'message': "something went wrong"}, 500
        else:
            try:
                patched_storage.update()
            except:
                return {'message': "something went wrong"}, 500
        return patched_storage.json(), 200


class StorageList(Resource):
    def get(self):
        connection = sqlite3.connect('./dbsqlite3.db')
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
