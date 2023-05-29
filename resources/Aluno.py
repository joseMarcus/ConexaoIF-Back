from flask import request
from flask_restful import Resource, marshal_with
from helpers.database import db
from helpers.logger import log
from model.pessoa import Pessoa, pessoa_fields
from model.aluno import Aluno, aluno_fields
from model.periodo import Periodo
from model.endereco import Endereco
from model.instituicao import Instituicao
from model.curso import Curso


class AlunoResource(Resource):
    @marshal_with(aluno_fields)
    def get(self, aluno_id=None):
        log.info("Get - Alunos")
        if aluno_id:
            aluno = Aluno.query.get(aluno_id)
            if aluno:
                return aluno, 200
            else:
                return {'message': 'Student not found'}, 404
        else:
            alunos = Aluno.query.all()
            return alunos, 200

    def post(self):
        log.info("Post - Alunos")
        data = request.json

        # Extract Coordenador data from the request JSON
        nome = data['nome']
        email = data['email']
        senha = data['senha']
        telefone = data['telefone']
        matricula = data['matricula']

        periodo_data = data.get('periodo')
        if periodo_data:
            periodo_semestrereferencia = periodo_data['semestrereferencia']
            periodo = Periodo(semestrereferencia=periodo_semestrereferencia)
        else:
            periodo = None

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
        aluno = Aluno(nome=nome, email=email, senha=senha, telefone=telefone, matricula=matricula,periodo=periodo, instituicao=instituicao)

        # Save Coordenador to the database
        db.session.add(aluno)
        db.session.commit()

        return {'message': 'Student created successfully'}, 201

    def put(self, aluno_id):
        log.info("Put - Alunos")
        data = request.json

        # Fetch the Coordenador from the database
        aluno = Aluno.query.get(aluno_id)

        if not aluno:
            return {'message': 'Student not found'}, 404

        # Update Coordenador attributes based on the request JSON
        if 'nome' in data:
            aluno.nome = data['nome']
        if 'email' in data:
            aluno.email = data['email']
        if 'senha' in data:
            aluno.senha = data['senha']
        if 'telefone' in data:
            aluno.telefone = data['telefone']
        if 'matricula' in data:
            aluno.matricula = data['matricula']
    

        # Save the updated Coordenador to the database
        db.session.commit()

        return {'message': 'Student updated successfully'}, 200

    def delete(self, aluno_id):
        log.info("Delete - Alunos")
        # Fetch the Coordenador from the database
        aluno = Aluno.query.get(aluno_id)

        if not aluno:
            return {'message': 'Student not found'}, 404

        # Delete the Coordenador from the database
        db.session.delete(aluno)
        db.session.commit()

        return {'message': 'Student deleted successfully'}, 200
