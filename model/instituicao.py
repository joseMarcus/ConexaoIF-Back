from flask_restful import fields
from helpers.database import db
from model.endereco import Endereco, endereco_fields
from model.curso import Curso, curso_fields

instituicao_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'endereco': fields.Nested(endereco_fields),
    'curso': fields.Nested(curso_fields)
}

class Instituicao(db.Model):
    __tablename__ = "instituicao"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'))
    endereco = db.relationship("Endereco", backref="instituicao")

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso = db.relationship("Curso", backref="instituicao")

    def __init__(self, nome, endereco: Endereco, curso: Curso):
        self.nome = nome
        self.endereco = endereco
        self.curso = curso

    def __repr__(self):
        return f'<Instituicao {self.nome}>'
