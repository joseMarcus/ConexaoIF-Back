from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.grupo import Grupo, grupo_fields
from model.coordenador import Coordenador


parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, help='Problema na conversão do título')
parser.add_argument('link', type=str, help='Problema na conversão do link')
parser.add_argument('semestreturma', type=str, help='Problema na conversão do semestre/turma')

parser.add_argument('coordenador', type=dict, required=True)


class GrupoResource(Resource):
    @marshal_with(grupo_fields)
    def get(self):
        log.info("Get - Grupos")
        grupos = Grupo.query.filter_by(excluido=False).all()
        return grupos, 200

    def post(self):
        log.info("Post - Grupos")
        args = parser.parse_args()
        titulo = args['titulo']
        link = args['link']
        semestreturma = args['semestreturma']

        coordenador_id = args['coordenador']['id']

        # Fetch Instituicao and Curso from the database
        coordenador = Coordenador.query.filter_by(id=coordenador_id, excluido=False).first()
        # Create Grupo instance
        grupo = Grupo(titulo=titulo, link=link, semestreturma=semestreturma, coordenador=coordenador)

        # Save Grupo to the database
        db.session.add(grupo)
        db.session.commit()

        return {'message': 'Group created successfully'}, 201

    
class GruposResource(Resource):

    def get(self, grupo_id):
        log.info("Get - Grupos")
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if (grupo is not None):
            return marshal(grupo, grupo_fields), 201
        else:
            return {'message': 'Grupo not found'}, 404
        
    def put(self, grupo_id):
        log.info("Put - Grupos")
        args = parser.parse_args()

        # Fetch the Grupo from the database
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if not grupo:
            return {'message': 'Group not found'}, 404

        # Update Grupo attributes based on the request arguments
        grupo.titulo = args.get('titulo', grupo.titulo)
        grupo.link = args.get('link', grupo.link)
        grupo.semestreturma = args.get('semestreturma', grupo.semestreturma)

        coordenador_id = args['coordenador']['id']
        if coordenador_id:
            grupo.coordenador = Coordenador.query.get(coordenador_id)
        # Save the updated Grupo to the database
        db.session.commit()

        return {'message': 'Group updated successfully'}, 200

    def delete(self, grupo_id):
        log.info("Delete - Grupos")
        # Fetch the Grupo from the database
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()

        if grupo is not None:
            grupo.excluido = True #para delete físico troca isso aqui por "db.session.delete(grupo)"
            db.session.commit()
            return {'message': 'Grupo deleted successfully'}, 200

        if not grupo:
            return {'message': 'Grupo not found'}, 404
