from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.professor import Professor, professor_fields

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('disciplina', type=str, help='Problema na conversão da disciplina')

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

        professor = Professor(nome=nome, email=email, senha=senha, telefone=telefone, disciplina=disciplina)
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

        professor = Professor.query.filter_by(id=professor_id, excluido_professor=False).first()
        if not professor:
            return {'message': 'Professor not found'}, 404

        if args['nome']:
            professor.nome = args['nome']
        if args['email']:
            professor.email = args['email']
        if args['senha']:
            professor.senha = args['senha']
        if args['telefone']:
            professor.telefone = args['telefone']
        if args['disciplina']:
            professor.disciplina = args['disciplina']

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
    