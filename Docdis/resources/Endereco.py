from flask_restful import Resource, reqparse, current_app, marshal, marshal_with
from sqlalchemy import exc

from helpers.database import db


from model.endereco import Endereco


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('cep', required=True)



class Enderecos(Resource):
    def get(self):
        current_app.logger.info("Get - Endereços")
        endereco = Endereco.query\
            .all()
        return endereco, 200

    def post(self):
        current_app.logger.info("Post - Endereços")
        try:
            # JSON
            args = parser.parse_args()
            cep = args['cep']

            # Endereco
            endereco = Endereco(cep)
            # Criação do Endereco.
            db.session.add(endereco)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            

        return 200

    def put(self, endereco_id):
        current_app.logger.info("Put - Endereço")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Endereço: %s:" % args)
            # Evento
            cep = args['cep']

            Endereco.query \
                .filter_by(id=endereco_id) \
                .update(dict(cep=cep))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 200

    def delete(self, endereco_id):
        current_app.logger.info("Delete - Endereço: %s:" % endereco_id)
        try:
            Endereco.query.filter_by(id=endereco_id).delete()
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 200