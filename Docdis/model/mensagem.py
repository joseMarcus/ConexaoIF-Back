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
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico

   
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)

    aluno = db.relationship('Aluno', backref='mensagens')
    grupo = db.relationship('Grupo', backref='mensagens')

    def __init__(self, texto, aluno, grupo):
        self.texto = texto
        self.aluno = aluno
        self.grupo = grupo
        self.excluido = False


    def __repr__(self):
        return f'<Mensagem {self.texto}>'
