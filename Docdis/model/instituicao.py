from flask_restful import fields
from helpers.database import db
from model.endereco import Endereco

instituicao_fields = {
    'id': fields.Integer,
    'nome': fields.String
}

class Instituicao(db.Model):
    __tablename__ = "instituicao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

    endereco = db.relationship("Endereco", backref="instituicao")

    def __init__(self, nome, endereco: Endereco):
        self.nome = nome
        self.endereco = endereco

    def __repr__(self):
        return f'<Instituicao {self.nome}>'