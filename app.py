from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from storage import Storage, StorageList
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'thisisnotasecretsecretkeyitsasecretkeythatisnotconsideredasecretsecretkey'
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Storage, '/api/storages/<string:name>')
api.add_resource(StorageList, '/api/storages')
api.add_resource(UserRegister, '/api/users/register')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
