from flask_restful import fields
from helpers.database import db


grupo_fields = {
    'id': fields.Integer,
    'titulo': fields.String,
    'link': fields.String,
}

class Grupo(db.Model):

    __tablename__ = "grupo"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    
    alunos = db.relationship("Aluno", secondary="alunogrupo", backref="grupos")
    coordenador_id = db.Column(db.Integer, db.ForeignKey('coordenador.id'))

    def __init__(self, titulo, link):
        self.titulo = titulo
        self.link = link

    def __repr__(self):
        return f'<Grupo {self.titulo}>'