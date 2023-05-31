from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

aluno_fields = {
    'id': fields.Integer,
    'matricula': fields.String,
}

class Aluno(Pessoa):
    __tablename__ = 'aluno'
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), primary_key=True)
    matricula = db.Column(db.String, nullable=False)
    excluido_aluno = db.Column(db.Boolean, default=False)  # Delete lógico

    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'), nullable=False)
    instituicao_id = db.Column(db.Integer, db.ForeignKey('instituicao.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    periodo = db.relationship('Periodo', backref='alunos')
    instituicao = db.relationship('Instituicao', backref='alunos')
    curso = db.relationship('Curso', backref='alunos')

    __mapper_args__ = {
        'polymorphic_identity': 'aluno'
    }

    def __init__(self, nome, email, senha, telefone, matricula, periodo, instituicao, curso):
        super().__init__(nome, email, senha, telefone)
        self.matricula = matricula
        self.periodo = periodo
        self.instituicao = instituicao
        self.curso = curso
        self.excluido_aluno = False

    def __repr__(self):
        return f'<Aluno {self.matricula}>'
