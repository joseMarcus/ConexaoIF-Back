from flask import request
from flask_restful import Resource, marshal_with
from helpers.database import db
from helpers.logger import log
from model.mensagem import Mensagem, mensagem_fields
from model.aluno import Aluno
from model.periodo import Periodo


class MensagemResource(Resource):
    @marshal_with(mensagem_fields)
    def get(self, mensagem_id=None):
        log.info("Get - Mensagens")
        if mensagem_id:
            mensagem = Mensagem.query.get(mensagem_id)
            if mensagem:
                return mensagem, 200
            else:
                return {'message': 'Mensagem not found'}, 404
        else:
            mensagens = Mensagem.query.all()
            return mensagens, 200

    def post(self):
        log.info("Post - Mensagens")
        data = request.json

        # Extract mensagem data from the request JSON
        texto = data['texto']
        aluno_id = data['aluno_id']
        periodo_id = data['periodo_id']

        # Fetch the aluno and periodo from the database
        aluno = Aluno.query.get(aluno_id)
        periodo = Periodo.query.get(periodo_id)

        if not aluno or not periodo:
            return {'message': 'Aluno or Periodo not found'}, 404

        # Create mensagem instance
        mensagem = Mensagem(texto=texto, aluno=aluno, periodo=periodo)

        # Save mensagem to the database
        db.session.add(mensagem)
        db.session.commit()

        return {'message': 'Mensagem created successfully'}, 201

    def put(self, mensagem_id):
        log.info("Put - Mensagens")
        data = request.json

        # Fetch the mensagem from the database
        mensagem = Mensagem.query.get(mensagem_id)

        if not mensagem:
            return {'message': 'Mensagem not found'}, 404

        # Update mensagem attributes based on the request JSON
        if 'texto' in data:
            mensagem.texto = data['texto']
        if 'aluno_id' in data:
            aluno_id = data['aluno_id']
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                return {'message': 'Aluno not found'}, 404
            mensagem.aluno = aluno
        if 'periodo_id' in data:
            periodo_id = data['periodo_id']
            periodo = Periodo.query.get(periodo_id)
            if not periodo:
                return {'message': 'Periodo not found'}, 404
            mensagem.periodo = periodo

        # Save the updated mensagem to the database
        db.session.commit()

        return {'message': 'Mensagem updated successfully'}, 200

    def delete(self, mensagem_id):
        log.info("Delete - Mensagens")
        # Fetch the mensagem from the database
        mensagem = Mensagem.query.get(mensagem_id)

        if not mensagem:
            return {'message': 'Mensagem not found'}, 404

        # Delete the mensagem from the database
        db.session.delete(mensagem)
        db.session.commit()

        return {'message': 'Mensagem deleted successfully'}, 200
