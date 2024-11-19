from . import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(120), nullable=False)
    document = db.Column(db.String(120), nullable=False)
