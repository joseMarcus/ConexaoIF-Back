from flask_restful import fields
from helpers.database import db


grupo_fields = {
    'id': fields.Integer,
    'titulo': fields.String,
    'link': fields.String,
    'semestreturma': fields.Integer
}

class Grupo(db.Model):

    __tablename__ = "grupo"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    semestreturma = db.Column(db.Integer, nullable=False)
    coordenador_id = db.Column(db.Integer, db.ForeignKey('coordenador.id'), nullable=False)
    alunos = db.relationship('Aluno', secondary='alunogrupo', backref=db.backref('grupos', lazy='dynamic'))

    def __init__(self, titulo, link, semestreturma, coordenador_id):
        self.titulo = titulo
        self.link = link
        self.semestreturma = semestreturma
        self.coordenador_id = coordenador_id

    def __repr__(self):
        return f'<Grupo {self.titulo}>'
