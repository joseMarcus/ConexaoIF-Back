from flask_restful import fields
from helpers.database import db


alunogrupo_fields = {
    'id': fields.Integer,
}

class AlunoGrupo(db.Model):

    __tablename__ = "alunogrupo"

    id = db.Column(db.Integer, primary_key=True)
    excluido = db.Column(db.Boolean, default=False)  # Delete lógico
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)

    aluno = db.relationship('Aluno', backref='alunosgrupo')
    grupo = db.relationship('Grupo', backref='alunosgrupo')

    def __init__(self, aluno, grupo):
        self.aluno = aluno
        self.grupo = grupo
        self.excluido = False

    def __repr__(self):
        return f'<AlunoGrupo {self.id}>'
