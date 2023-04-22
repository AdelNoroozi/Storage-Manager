from flask_restful import Resource, reqparse

from models.cargo import CargoModel


class Cargo(Resource):
    cargo_parser = reqparse.RequestParser()
    cargo_parser.add_argument('quantity',
                              type=int,
                              required=True,
                              help="missing field: quantity")

    def get(self, name):
        cargo = CargoModel.find_by_name(name)
        if not cargo:
            return {'message': "cargo not found"}, 404
        else:
            return cargo.json(), 200

    def post(self, name):
        if CargoModel.find_by_name(name):
            return {'message': f'cargo with the name {name} already exists'}, 401
        data = Cargo.cargo_parser.parse_args()
        quantity = data['quantity']
        cargo = CargoModel(name=name, quantity=quantity)
        try:
            cargo.save()
        except:
            return {'message': 'something went wrong'}, 500
        return cargo.json(), 201

    def put(self, name):
        data = Cargo.cargo_parser.parse_args()
        quantity = data['quantity']
        cargo = CargoModel.find_by_name(name)
        if cargo is None:
            try:
                cargo = CargoModel(name=name, quantity=quantity)
            except:
                return {'message': 'something went wrong'}, 500
        else:
            try:
                cargo.quantity = quantity
            except:
                return {'message': 'something went wrong'}, 500
        cargo.save()
        return cargo.json(), 200
