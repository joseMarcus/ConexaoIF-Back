from flask import request
from flask_restful import Resource, marshal_with, reqparse, marshal
from helpers.database import db
from helpers.logger import log
from model.mensagem import Mensagem, mensagem_fields
from model.aluno import Aluno
from model.grupo import Grupo

parser = reqparse.RequestParser()
parser.add_argument('texto', type=str, help='Problema na conversão do texto')
parser.add_argument('aluno', type=dict, required=True)
parser.add_argument('grupo', type=dict, required=True)

class MensagemResource(Resource):
    @marshal_with(mensagem_fields)
    def get(self):
        log.info("Get - Mensagens")
        mensagens = Mensagem.query.filter_by(excluido=False).all()
        return mensagens, 200

    def post(self):
        log.info("Post - Mensagens")
        args = parser.parse_args()

        texto = args['texto']

        aluno_id = args['aluno']['id']
        grupo_id = args['grupo']['id']

        aluno = Aluno.query.filter_by(id=aluno_id, excluido=False).first()
        grupo = Grupo.query.filter_by(id=grupo_id, excluido=False).first()



        if not aluno or not grupo:
            return {'message': 'Aluno or Grupo not found'}, 404

        mensagem = Mensagem(texto=texto, aluno=aluno, grupo=grupo)

        db.session.add(mensagem)
        db.session.commit()

        return {'message': 'Mensagem created successfully'}, 201

    
class MensagensResource(Resource):

    def get(self, mensagem_id):
        log.info("Get - Mensagens")
        mensagem = Mensagem.query.filter_by(id=mensagem_id, excluido=False).first()

        if (mensagem is not None):
            return marshal(mensagem, mensagem_fields), 201
        else:
            return {'message': 'Mensagem not found'}, 404
        
    def put(self, mensagem_id):
        log.info("Put - Mensagens")
        args = parser.parse_args()

        mensagem = Mensagem.query.filter_by(id=mensagem_id, excluido=False).first()
        if not mensagem:
            return {'message': 'Mensagem not found'}, 404

        if args['texto']:
            mensagem.texto = args['texto']

        aluno_id = args['aluno']['id']
        if aluno_id:
            mensagem.aluno = Aluno.query.get(aluno_id)

        grupo_id = args['grupo']['id']
        if grupo_id:
            mensagem.grupo = Grupo.query.get(grupo_id)
        db.session.commit()

        return {'message': 'Mensagem updated successfully'}, 200

    def delete(self, mensagem_id):
        log.info("Delete - Mensagens")
        mensagem = Mensagem.query.filter_by(id=mensagem_id, excluido=False).first()

        if mensagem is not None:
            mensagem.excluido = True #para delete físico troca isso aqui por "db.session.delete(mensagem)"
            db.session.commit()
            return {'message': 'Mensagem deleted successfully'}, 200

        if not mensagem:
            return {'message': 'Mensagem not found'}, 404
