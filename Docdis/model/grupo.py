from flask_restful import fields
from helpers.database import db
from model.alunogrupo import AlunoGrupo



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
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico
    
    coordenador_id = db.Column(db.Integer, db.ForeignKey('coordenador.id'), nullable=False)
    coordenador = db.relationship('Coordenador', backref='grupos')


    def __init__(self, titulo, link, semestreturma, coordenador):
        self.titulo = titulo
        self.link = link
        self.semestreturma = semestreturma
        self.coordenador = coordenador
        self.excluido = False

    def __repr__(self):
        return f'<Grupo {self.titulo}>'
