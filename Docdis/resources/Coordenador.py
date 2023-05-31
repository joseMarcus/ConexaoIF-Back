from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.coordenador import Coordenador, coordenador_fields
from model.instituicao import Instituicao
from model.curso import Curso


parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('disciplina', type=str, help='Problema na conversão da disciplina')
parser.add_argument('registrodeTrabalho', type=str, help='Problema na conversão do registro de trabalho')

parser.add_argument('instituicao', type=dict, required=True)
parser.add_argument('curso', type=dict, required=True)


class CoordenadorResource(Resource):
    @marshal_with(coordenador_fields)
    def get(self):
        log.info("Get - Coordenadores")
        coordenadores = Coordenador.query.filter_by(excluido_coordenador=False).all()
        return coordenadores, 200

    def post(self):
        log.info("Post - Coordenadores")

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']
        disciplina = args['disciplina']
        registrodeTrabalho = args['registrodeTrabalho']

        # Extract Instituicao and Curso data from the request JSON
        instituicao_id = args['instituicao']['id']
        curso_id = args['curso']['id']

        # Fetch Instituicao and Curso from the database
        instituicao = Instituicao.query.filter_by(id=instituicao_id, excluido=False).first()
        curso = Curso.query.filter_by(id=curso_id, excluido=False).first()

        if not instituicao or not curso:
            return {'message': 'Invalid Instituicao or Curso'}, 400

        # Create Coordenador instance
        coordenador = Coordenador(nome=nome, email=email, senha=senha, telefone=telefone,
                                 disciplina=disciplina, registrodeTrabalho=registrodeTrabalho,
                                 instituicao=instituicao, curso=curso)

        # Save Coordenador to the database
        db.session.add(coordenador)
        db.session.commit()

        return {'message': 'Coordenador created successfully'}, 201

    
class CoordenadoresResource(Resource):

    def get(self, coordenador_id):
        log.info("Get - Coordenadores")
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido_coordenador=False).first()

        if (coordenador is not None):
            return marshal(coordenador, coordenador_fields), 201
        else:
            return {'message': 'Coordenador not found'}, 404
        
    def put(self, coordenador_id):
        log.info("Put - Coordenadores")
        data = request.json

        # Fetch the Coordenador from the database
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido_coordenador=False).first()

        if not coordenador:
            return {'message': 'Coordenador not found'}, 404

        # Update Coordenador attributes based on the request JSON
        coordenador.nome = data.get('nome', coordenador.nome)
        coordenador.email = data.get('email', coordenador.email)
        coordenador.senha = data.get('senha', coordenador.senha)
        coordenador.telefone = data.get('telefone', coordenador.telefone)
        coordenador.disciplina = data.get('disciplina', coordenador.disciplina)
        coordenador.registrodeTrabalho = data.get('registrodeTrabalho', coordenador.registrodeTrabalho)

        instituicao_id = data['instituicao'].get('id')
        if instituicao_id:
            coordenador.instituicao = Instituicao.query.get(instituicao_id)

        curso_id = data['curso'].get('id')
        if curso_id:
            coordenador.curso = Curso.query.get(curso_id)

        # Save the updated Coordenador to the database
        db.session.commit()

        return {'message': 'Coordenador updated successfully'}, 200

    def delete(self, coordenador_id):
        log.info("Delete - Coordenadores")
        # Fetch the Coordenador from the database
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido_coordenador=False).first()

        if coordenador is not None:
            coordenador.excluido_coordenador = True #para delete físico troca isso aqui por "db.session.delete(coordenador)"
            db.session.commit()
            return {'message': 'Coordenador deleted successfully'}, 200

        if not coordenador:
            return {'message': 'Coordenador not found'}, 404
