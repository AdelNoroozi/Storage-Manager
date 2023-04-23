from db import db


class CargoModel(db.Model):
    __tablename__ = 'cargos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    storage_id = db.Column(db.Integer, db.ForeignKey('storages.id'))
    storage = db.relationship('StorageModel')

    def __init__(self, name, quantity, storage_id):
        self.name = name
        self.quantity = quantity
        self.storage_id = storage_id

    def json(self):
        return {'name': self.name, 'quantity': self.quantity, 'storage_id': self.storage_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
