from flask import Flask, Blueprint,jsonify
from flask_restful import Api
from helpers.database import db, migrate
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from helpers.cors import cors
from bot_email.enviar_email import EmailResource
from resources.Pessoa import PessoaResource, PessoasResource
from resources.Aluno import AlunoResource, AlunosResource
from resources.Coordenador import CoordenadorResource, CoordenadoresResource
from resources.Curso import CursoResource, CursosResource
from resources.Endereco import EnderecoResource, EnderecosResource
from resources.Grupo import GrupoResource, GruposResource
from resources.Instituicao import InstituicaoResource, InstituicoesResource
from resources.Periodo import PeriodoResource, PeriodosResource
from resources.Professor import ProfessorResource, ProfessoresResource
from flask_cors import CORS



app = Flask(__name__)
CORS(app)



# Criado um objeto de configuração com base na variável de ambiente FLASK_ENV
if app.config['ENV'] == 'production':
    app.config.from_object(ProductionConfig())
elif app.config['ENV'] == 'testing':
    app.config.from_object(TestingConfig())
else:
    app.config.from_object(DevelopmentConfig())


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/IFPB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api')

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)



api.add_resource(PessoaResource, '/pessoa')
api.add_resource(PessoasResource, '/pessoa/<pessoa_id>')

api.add_resource(AlunoResource, '/aluno')
api.add_resource(AlunosResource, '/aluno/<aluno_id>')

api.add_resource(CoordenadorResource, '/coordenador')
api.add_resource(CoordenadoresResource, '/coordenador/<coordenador_id>')

api.add_resource(CursoResource, '/curso')
api.add_resource(CursosResource, '/curso/<curso_id>')

api.add_resource(EnderecoResource, '/endereco')
api.add_resource(EnderecosResource, '/endereco/<endereco_id>')

api.add_resource(GrupoResource, '/grupo')
api.add_resource(GruposResource, '/grupo/<int:grupo_id>')

api.add_resource(InstituicaoResource, '/instituicao')
api.add_resource(InstituicoesResource, '/instituicao/<int:instituicao_id>')
api.add_resource(PeriodoResource, '/periodo')
api.add_resource(PeriodosResource, '/periodo/<int:periodo_id>')
api.add_resource(ProfessorResource, '/professor')
api.add_resource(ProfessoresResource, '/professor/<int:professor_id>')









app.register_blueprint(api_bp)
api.add_resource(EmailResource, '/send')


if __name__ == '__main__':
    app.run()