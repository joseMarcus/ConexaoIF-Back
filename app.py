from flask import Flask, Blueprint
from flask_restful import Api
from helpers.database import db, migrate
from helpers.cors import cors
from resources.Pessoa import PessoaResource, PessoasResource
from resources.Coordenador import CoordenadorResource
from resources.Aluno import AlunoResource
from resources.Grupo import GrupoResource
from resources.Mensagem import MensagemResource
from config import DevelopmentConfig, ProductionConfig, TestingConfig


app = Flask(__name__)



# Criado um objeto de configuração com base na variável de ambiente FLASK_ENV
if app.config['ENV'] == 'production':
    app.config.from_object(ProductionConfig())
elif app.config['ENV'] == 'testing':
    app.config.from_object(TestingConfig())
else:
    app.config.from_object(DevelopmentConfig())


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/models"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api')

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)



api.add_resource(PessoaResource, '/pessoas')
api.add_resource(PessoasResource, '/pessoas/<pessoa_id>')
api.add_resource(CoordenadorResource, '/coordenador', '/coordenador/<int:coordenador_id>')
api.add_resource(AlunoResource, '/aluno', '/aluno/<int:aluno_id>')
api.add_resource(GrupoResource, '/grupo', '/grupo/<int:grupo_id>')
api.add_resource(MensagemResource, '/mensagem', '/mensagem/<int:mensagem_id>')



app.register_blueprint(api_bp)



if __name__ == '__main__':
    app.run()