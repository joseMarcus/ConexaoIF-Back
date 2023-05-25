from flask_restful import fields
from helpers.database import db
from model.aluno import Aluno
from model.periodo import Periodo


mensagem_fields = {
    'id': fields.Integer,
    'texto': fields.String,

}

class Mensagem(db.Model):
    __tablename__ = "mensagem"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String, nullable=False)
   
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    aluno = db.relationship("Aluno", backref="mensagens")
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    periodo = db.relationship("Periodo", backref="mensagens")

    def __init__(self, texto):
        self.texto = texto

    def __repr__(self):
        return f'<Mensagem {self.texto}>'