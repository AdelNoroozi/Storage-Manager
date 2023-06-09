from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.cargo import *
from security import authenticate, identity
from resources.storage import *
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbsqlite3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisisnotasecretsecretkeyitsasecretkeythatisnotconsideredasecretsecretkey'
api = Api(app)
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Storage, '/api/storages/<string:name>')
api.add_resource(Cargo, '/api/cargos/<string:name>')
api.add_resource(StorageList, '/api/storages')
api.add_resource(CargoList, '/api/cargos')
api.add_resource(UserRegister, '/api/users/register')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5001, debug=True)
