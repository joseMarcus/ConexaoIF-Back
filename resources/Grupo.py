from flask import request
from flask_restful import Resource, marshal_with
from helpers.database import db
from helpers.logger import log
from model.grupo import Grupo, grupo_fields


class GrupoResource(Resource):
    @marshal_with(grupo_fields)
    def get(self, grupo_id=None):
        log.info("Get - Grupos")
        if grupo_id:
            grupo = Grupo.query.get(grupo_id)
            if grupo:
                return grupo, 200
            else:
                return {'message': 'Group not found'}, 404
        else:
            grupos = Grupo.query.all()
            return grupos, 200

    def post(self):
        log.info("Post - Grupos")
        data = request.json

        # Extract Grupo data from the request JSON
        titulo = data['titulo']
        link = data['link']
        semestreturma = data['semestreturma']

        coordenador_id = data['coordenador_id']

        # Create Grupo instance
        grupo = Grupo(titulo=titulo, link=link, semestreturma=semestreturma, coordenador_id=coordenador_id)

        # Save Grupo to the database
        db.session.add(grupo)
        db.session.commit()

        return {'message': 'Group created successfully'}, 201

    def put(self, grupo_id):
        log.info("Put - Grupos")
        data = request.json

        # Fetch the Grupo from the database
        grupo = Grupo.query.get(grupo_id)

        if not grupo:
            return {'message': 'Group not found'}, 404

        # Update Grupo attributes based on the request JSON
        if 'titulo' in data:
            grupo.titulo = data['titulo']
        if 'link' in data:
            grupo.link = data['link']
        if 'semestreturma' in data:
            grupo.semestreturma = data['semestreturma']

        # Save the updated Grupo to the database
        db.session.commit()

        return {'message': 'Group updated successfully'}, 200

    def delete(self, grupo_id):
        log.info("Delete - Grupos")
        # Fetch the Grupo from the database
        grupo = Grupo.query.get(grupo_id)

        if not grupo:
            return {'message': 'Group not found'}, 404

        # Delete the Grupo from the database
        db.session.delete(grupo)
        db.session.commit()

        return {'message': 'Group deleted successfully'}, 200
