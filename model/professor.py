from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

professor_fields = {
    'id': fields.Integer,
    'disciplina': fields.String
   
}
class Professor(Pessoa):
    __tablename__ = 'professor'
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), primary_key=True)
    disciplina = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }

    def __init__(self, nome, email, senha, telefone, disciplina):
        super().__init__(nome, email, senha, telefone)
        self.disciplina = disciplina
    
    def __repr__(self):
        return f'<Professor {self.disciplina}>'
