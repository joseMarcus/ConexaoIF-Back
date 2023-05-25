from flask_restful import fields
from helpers.database import db
from model.instituicao import Instituicao


curso_fields = {
    'id': fields.Integer,
    'nome': fields.String,
}


class Curso(db.Model):

    __tablename__ = "curso"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

    instituicao_id = db.Column(db.Integer, db.ForeignKey('instituicao.id'))
    instituicao = db.relationship("Instituicao", backref="cursos")


    def __init__(self, nome, instituicao: Instituicao):
        self.nome = nome
        self.instituicao = instituicao


    def __repr__(self):
        return f'<Curso {self.nome}>'

