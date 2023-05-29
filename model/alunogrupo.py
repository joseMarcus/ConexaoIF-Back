from flask_restful import fields
from helpers.database import db


alunogrupo_fields = {
    'id': fields.Integer,
}

class AlunoGrupo(db.Model):

    __tablename__ = "alunogrupo"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), primary_key=True)

    def __init__(self, aluno_id, grupo_id):
        self.aluno_id = aluno_id
        self.grupo_id = grupo_id

    def __repr__(self):
        return f'<AlunoGrupo {self.id}>'
