from flask_restful import Resource

from models.cargo import CargoModel


class Cargo(Resource):
    def get(self, name):
        cargo = CargoModel.find_by_name(name)
        if not cargo:
            return {'message': "cargo not found"}
        else:
            return cargo.json()
