from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.professor import Professor, professor_fields
from model.curso import Curso, curso_fields

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('disciplina', type=str, help='Problema na conversão da disciplina')

parser.add_argument('curso', type=dict, required=True)

class ProfessorResource(Resource):
    @marshal_with(professor_fields)
    def get(self, professor_id=None):
        log.info("Get - Professores")        
        professores = Professor.query.filter_by(excluido_professor=False).all()
        return professores, 200

    def post(self):
        log.info("Post - Professores")
        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        disciplina = args['disciplina']

        # Extract Curso data from the request JSON
        curso_professor_id = args['curso']['id']

        # Fetch Instituicao and Curso from the database
        curso = Curso.query.filter_by(id=curso_professor_id, excluido=False).first()

        professor = Professor(nome=nome, email=email, senha=senha, telefone=telefone, disciplina=disciplina, curso=curso)
        db.session.add(professor)
        db.session.commit()

        return {'message': 'Professor created successfully'}, 201

    
class ProfessoresResource(Resource):

    def get(self, professor_id):
        log.info("Get - Professores")        
        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()

        if (professor is not None):
            return marshal(professor, professor_fields), 201
        else:
            return {'message': 'Professor not found'}, 404
        
    def put(self, professor_id):
        log.info("Put - Professores")

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        disciplina = args['disciplina']

        # Fetch the Professor from the database
        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()

        if not professor:
            return {'message': 'Professor not found'}, 404

        # Update Professor attributes based on the request args
        if nome:
            professor.nome = nome
        if email:
            professor.email = email
        if senha:
            professor.senha = senha
        if telefone:
            professor.telefone = telefone
        if disciplina:
            professor.disciplina = disciplina


        curso_professor_id = args['curso']['id']
        if curso_professor_id:
            professor.curso = Curso.query.get(curso_professor_id)

        # Save the updated Professor to the database
        db.session.commit()

        return {'message': 'Professor updated successfully'}, 200


    def delete(self, professor_id):
        log.info("Delete - Professores")        
        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()

        if professor is not None:
            professor.excluido_professor = True #para delete físico troca isso aqui por "db.session.delete(professor)"
            db.session.commit()
            return {'message': 'Professor deleted successfully'}, 200

        if not professor:
            return {'message': 'Professor not found'}, 404
    