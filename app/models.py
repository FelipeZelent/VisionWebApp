from . import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    document = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)  # Campo para a descrição da imagem
