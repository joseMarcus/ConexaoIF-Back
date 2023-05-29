from flask import request
from flask_restful import Resource, marshal_with
from helpers.database import db
from helpers.logger import log
from model.coordenador import Coordenador, coordenador_fields
from model.endereco import Endereco
from model.instituicao import Instituicao
from model.curso import Curso

from model.endereco import Endereco
#from model.aluno import *
from model.alunogrupo import *
from model.coordenador import *
from model.curso import *
from model.grupo import *
from model.instituicao import *
from model.periodo import *
from model.professor import *
from model.mensagem import Mensagem, mensagem_fields

class CoordenadorResource(Resource):
    @marshal_with(coordenador_fields)
    def get(self, coordenador_id=None):
        log.info("Get - Coordenadores")
        if coordenador_id:
            coordenador = Coordenador.query.get(coordenador_id)
            if coordenador:
                return coordenador, 200
            else:
                return {'message': 'Coordenador not found'}, 404
        else:
            coordenadores = Coordenador.query.all()
            return coordenadores, 200

    def post(self):
        log.info("Post - Coordenadores")
        data = request.json

        # Extract Coordenador data from the request JSON
        nome = data['nome']
        email = data['email']
        senha = data['senha']
        telefone = data['telefone']
        disciplina = data['disciplina']
        registrodeTrabalho = data['registrodeTrabalho']

        # Extract Instituicao data from the request JSON
        instituicao_data = data.get('instituicao')
        if instituicao_data:
            instituicao_nome = instituicao_data['nome']
            endereco_data = instituicao_data.get('endereco')
            curso_data = instituicao_data.get('curso')
            if curso_data and endereco_data:
                rua = endereco_data['rua']
                bairro = endereco_data['bairro']
                cep = endereco_data['cep']
                numero = endereco_data['numero']
                complemento = endereco_data['complemento']
                endereco = Endereco(rua=rua, bairro=bairro, cep=cep, numero=numero, complemento=complemento)
                curso_nome = curso_data['nome']
                curso = Curso(nome=curso_nome)
            else:
                endereco = None
                curso = None

            instituicao = Instituicao(nome=instituicao_nome, endereco=endereco, curso=curso)
        else:
            instituicao = None

        # Create Coordenador instance
        coordenador = Coordenador(nome=nome, email=email, senha=senha, telefone=telefone,
                                 disciplina=disciplina, registrodeTrabalho=registrodeTrabalho, instituicao=instituicao)

        # Save Coordenador to the database
        db.session.add(coordenador)
        db.session.commit()

        return {'message': 'Coordenador created successfully'}, 201

    def put(self, coordenador_id):
        log.info("Put - Coordenadores")
        data = request.json

        # Fetch the Coordenador from the database
        coordenador = Coordenador.query.get(coordenador_id)

        if not coordenador:
            return {'message': 'Coordenador not found'}, 404

        # Update Coordenador attributes based on the request JSON
        if 'nome' in data:
            coordenador.nome = data['nome']
        if 'email' in data:
            coordenador.email = data['email']
        if 'senha' in data:
            coordenador.senha = data['senha']
        if 'telefone' in data:
            coordenador.telefone = data['telefone']
        if 'disciplina' in data:
            coordenador.disciplina = data['disciplina']
        if 'registrodeTrabalho' in data:
            coordenador.registrodeTrabalho = data['registrodeTrabalho']

        # Save the updated Coordenador to the database
        db.session.commit()

        return {'message': 'Coordenador updated successfully'}, 200

    def delete(self, coordenador_id):
        log.info("Delete - Coordenadores")
        # Fetch the Coordenador from the database
        coordenador = Coordenador.query.get(coordenador_id)

        if not coordenador:
            return {'message': 'Coordenador not found'}, 404

        # Delete the Coordenador from the database
        db.session.delete(coordenador)
        db.session.commit()

        return {'message': 'Coordenador deleted successfully'}, 200
