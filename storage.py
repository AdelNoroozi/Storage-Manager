from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
import sqlite3


class Storage(Resource):
    storage_parser = reqparse.RequestParser()
    storage_parser.add_argument('is_available',
                                type=str,
                                required=True,
                                help="missing field: is_available")

    def get(self, name):
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
        else:
            return {'message': "item not found"}, 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, storages), None) is not None:
            return {'message': f'storage with name {name} already exists'}, 400
        data = Storage.storage_parser.parse_args()  # by using 'force = True' we can bypass content type header in our request, however it,s dangerous, and it is only useful for easier testing
        storage = {'name': name, 'is_available': data['is_available']}
        storages.append(storage)
        return storage, 201

    @jwt_required()
    def delete(self, name):
        global storages
        storage = next(filter(lambda x: x['name'] == name, storages), None)
        if storage is None:
            return {'message': 'storage not found'}, 404
        else:
            storages = list(filter(lambda x: x['name'] != name, storages))
            return {'message': f'storage with name {name} deleted'}, 200

    @jwt_required()
    def put(self, name):
        data = Storage.storage_parser.parse_args()
        storage = next(filter(lambda x: x['name'] == name, storages), None)
        if storage is None:
            storage = {'name': name, 'is_available': data['is_available']}
            storages.append(storage)
        else:
            storage.update(data)
        return storage, 200


class StorageList(Resource):
    def get(self):
        return {'storages': storages}
