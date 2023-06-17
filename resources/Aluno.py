from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.aluno import Aluno, aluno_fields
from model.periodo import Periodo
from model.curso import Curso

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('matricula', type=str, help='Problema na conversão da matrícula')

parser.add_argument('periodo', type=dict, required=True)
parser.add_argument('curso', type=dict, required=True)

class AlunoResource(Resource):
    @marshal_with(aluno_fields)
    def get(self):
        log.info("Get - Alunos")
        alunos = Aluno.query.filter_by(excluido_aluno=False).all()
        return alunos, 200

    def post(self):
        log.info("Post - Alunos")

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        matricula = args['matricula']

        # Fetch the associated objects based on their IDs
        periodo_id = args['periodo']['id']
        curso_id = args['curso']['id']

        periodo = Periodo.query.filter_by(id=periodo_id, excluido=False).first()
        curso = Curso.query.filter_by(id=curso_id, excluido=False).first()

        if not periodo or not curso:
            return {'message': 'Invalid Periodo or Curso'}, 400

        # Create Aluno instance
        aluno = Aluno(nome=nome, email=email, senha=senha, telefone=telefone, matricula=matricula,
                      periodo=periodo, curso=curso)

        # Save Aluno to the database
        db.session.add(aluno)
        db.session.commit()

        return {'message': 'Student created successfully'}, 201

    
class AlunosResource(Resource):

    def get(self, aluno_id):
        log.info("Get - Alunos")
        aluno = Aluno.query.filter_by(id=aluno_id, excluido_aluno=False).first()

        if (aluno is not None):
            return marshal(aluno, aluno_fields), 201
        else:
            return {'message': 'Student not found'}, 404

    def put(self, aluno_id):
        log.info("Put - Alunos")

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        matricula = args['matricula']

        # Fetch the Aluno from the database
        aluno = Aluno.query.filter_by(id=aluno_id, excluido_aluno=False).first()

        if not aluno:
            return {'message': 'Student not found'}, 404

        # Update Aluno attributes based on the request args
        if nome:
            aluno.nome = nome
        if email:
            aluno.email = email
        if senha:
            aluno.senha = senha
        if telefone:
            aluno.telefone = telefone
        if matricula:
            aluno.matricula = matricula

        # Fetch the associated objects based on their IDs if provided
        periodo_id = args['periodo']['id']
        if periodo_id:
            aluno.periodo = Periodo.query.get(periodo_id)


        curso_id = args['curso']['id']
        if curso_id:
            aluno.curso = Curso.query.get(curso_id)

        # Save the updated Aluno to the database
        db.session.commit()

        return {'message': 'Student updated successfully'}, 200

    def delete(self, aluno_id):
        log.info("Delete - Alunos")
        # Fetch the Aluno from the database
        aluno = Aluno.query.filter_by(id=aluno_id, excluido_aluno=False).first()

        if aluno is not None:
            aluno.excluido_aluno = True #para delete físico troca isso aqui por "db.session.delete(aluno)"
            db.session.commit()
            return {'message': 'Aluno deleted successfully'}, 200

        if not aluno:
            return {'message': 'Aluno not found'}, 404
    