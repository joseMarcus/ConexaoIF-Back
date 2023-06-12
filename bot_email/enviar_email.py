from flask_restful import Resource
from flask import request
from bot_email.email_utils import enviar_email

class EmailResource(Resource):
    def post(self):
        titulo_grupo = request.form.get('titulo_grupo')
        mensagem_manual = request.form.get('mensagem_manual')

        result = enviar_email(titulo_grupo, mensagem_manual)

        if result:
            return {'message': 'Mensagem enviada com sucesso!'}
        else:
            return {'message': 'Erro ao enviar mensagem.'}
