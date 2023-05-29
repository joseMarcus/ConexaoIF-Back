from flask_restful import Resource, reqparse, marshal_with, marshal
from helpers.database import db
from flask_httpauth import HTTPBasicAuth

from model.pessoa import Pessoa, pessoa_fields
from model.endereco import Endereco
from model.aluno import *
from model.alunogrupo import *
from model.coordenador import *
from model.curso import *
from model.grupo import *
from model.instituicao import *
from model.periodo import *
from model.professor import *
from model.mensagem import Mensagem, mensagem_fields

from helpers.logger import log

auth = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('email', type=str, help='Problema na conversão do email')
parser.add_argument('senha', type=str, help='Problema na conversão da senha')
parser.add_argument('telefone', type=str, help='Problema na conversão do telefone')
parser.add_argument('endereco', type=dict, required=True)


@auth.verify_password
def verify_password(username, password):
    # Aqui você deve verificar se o nome de usuário e a senha fornecidos são válidos
    if username == 'user' and password == 'password':
        return True
    return False

class PessoaResource(Resource):
    @auth.login_required
    @marshal_with(pessoa_fields)
    def get(self):
        pessoas = Pessoa.query.filter_by(excluido=False).all()
        return (pessoas, 201)
    
        
    @auth.login_required
    @marshal_with(pessoa_fields)  
    def post(self):
        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']

        enderecoArgs = args['endereco']
        rua = enderecoArgs['rua']
        bairro = enderecoArgs['bairro']
        cep = enderecoArgs['cep']
        numero = enderecoArgs['numero']
        complemento = enderecoArgs['complemento']

        endereco = Endereco(rua, bairro, cep, numero, complemento)
        
        pessoa = Pessoa(nome, email, senha, telefone, endereco)

        db.session.add(pessoa)
        db.session.commit()

        return pessoa, 201
    
class PessoasResource(Resource):
    @auth.login_required

    def get(self, pessoa_id):
        log.info("Identificador de pessoa: " + pessoa_id)
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if (pessoa is not None):
            return marshal(pessoa, pessoa_fields), 201
        else:
            mensagem = Mensagem('Pessoa não encontrada', 1)
            return marshal(mensagem, mensagem_fields), 404
    @auth.login_required

    @marshal_with(pessoa_fields)
    def put(self, pessoa_id):

        args = parser.parse_args()
        nome = args['nome']
        email = args['email']
        senha = args['senha']
        telefone = args['telefone']


        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if pessoa  is not None:
            pessoa.nome = nome
            pessoa.email = email
            pessoa.senha = senha
            pessoa.telefone = telefone



            db.session.add(pessoa)
            db.session.commit()

            return marshal(pessoa, pessoa_fields), 201

        else:
            mensagem = Mensagem('Pessoa não encontrada', 1)
            return marshal(mensagem, mensagem_fields), 404
        
        return pessoa
    @auth.login_required

    def delete(self, pessoa_id):
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if pessoa is not None:
            pessoa.excluido = True #para delete físico troca isso aqui por "db.session.delete(pessoa)"
            db.session.commit()

            mensagem = Mensagem('Pessoa excluída com sucesso', 0)
            return marshal(mensagem, mensagem_fields), 200

        else:
            mensagem = Mensagem('Pessoa não encontrada', 1)
            return marshal(mensagem, mensagem_fields), 404
