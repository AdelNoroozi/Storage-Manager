from db import db


class CargoModel(db.Model):
    __tablename__ = 'cargos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def json(self):
        return {'name': self.name, 'quantity': self.quantity}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
