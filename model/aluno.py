from flask_restful import fields
from helpers.database import db
from model.pessoa import Pessoa

aluno_fields = {
    'id': fields.Integer,
    'matricula': fields.String
   
}
class Aluno(Pessoa):
    __tablename__ = 'aluno'
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), primary_key=True)
    matricula = db.Column(db.String, nullable=False)

    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    periodo = db.relationship("Periodo", backref="alunos", foreign_keys=[periodo_id])


    instituicao_id = db.Column(db.Integer, db.ForeignKey('instituicao.id'))
    instituicao = db.relationship("Instituicao", backref="alunos")

    __mapper_args__ = {
        'polymorphic_identity': 'aluno'
    }

    def __init__(self, nome, email, senha, telefone, matricula, periodo, instituicao):
        super().__init__(nome, email, senha, telefone)
        self.matricula = matricula
        self.periodo = periodo
        self.instituicao = instituicao


    def __repr__(self):
        return f'<Aluno {self.matricula}>'
