from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

storages = []


class Storage(Resource):
    def get(self, name):
        storage = next(filter(lambda x: x['name'] == name, storages), None)
        return {'storage': storage}, 200 if storage else 404

    def post(self, name):
        data = request.get_json()  # by using 'force = True' we can bypass content type header in our request, however it,s dangerous and it is only useful for easier testing
        storage = {'name': name, 'is_available': data['is_available']}
        storages.append(storage)
        return storage, 201


class StorageList(Resource):
    def get(self):
        return {'storages': storages}


api.add_resource(Storage, '/api/storages/<string:name>')
api.add_resource(StorageList, '/api/storages')

app.run(port=5001, debug=True)
