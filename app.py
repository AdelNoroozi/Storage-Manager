from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'thisisnotasecretsecretkeyitsasecretkeythatisnotconsideredasecretsecretkey'
api = Api(app)
jwt = JWT(app, authenticate, identity)
storages = []


class Storage(Resource):
    def get(self, name):
        storage = next(filter(lambda x: x['name'] == name, storages), None)
        return {'storage': storage}, 200 if storage else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, storages), None) is not None:
            return {'message': f'storage with name {name} already exists'}, 400
        parser = reqparse.RequestParser()
        parser.add_argument('is_available',
                            type=str,
                            required=True,
                            help="missing field: is_available")

        data = parser.parse_args()  # by using 'force = True' we can bypass content type header in our request, however it,s dangerous and it is only useful for easier testing
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
        parser = reqparse.RequestParser()
        parser.add_argument('is_available',
                            type=str,
                            required=True,
                            help="missing field: is_available"
                            )
        data = parser.parse_args()
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


api.add_resource(Storage, '/api/storages/<string:name>')
api.add_resource(StorageList, '/api/storages')

app.run(port=5001, debug=True)
