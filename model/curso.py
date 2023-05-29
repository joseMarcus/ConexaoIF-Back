from flask_restful import fields
from helpers.database import db


curso_fields = {
    'id': fields.Integer,
    'nome': fields.String,
}


class Curso(db.Model):

    __tablename__ = "curso"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)



    def __init__(self, nome):
        self.nome = nome


    def __repr__(self):
        return f'<Curso {self.nome}>'

