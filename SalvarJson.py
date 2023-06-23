from flask import Blueprint, jsonify, request
import os
import json
import tempfile
from Utils import load_emails

api_bp = Blueprint('api', __name__)


def load_emails():
    file_path = os.path.join(os.path.dirname(__file__), 'lista.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


@api_bp.route('/get_emails', methods=['GET'])
def get_emails():
    try:
        emails_data = load_emails()  # Carrega os dados do arquivo JSON
        print(emails_data)  # Exibe os dados carregados do arquivo JSON

        if 'emails' not in emails_data:
            return jsonify({'message': 'Nenhum email encontrado'})  # Retorna uma resposta JSON caso não haja emails

        emails = emails_data['emails']  # Acessa a lista de emails no JSON

        return jsonify(emails)  # Retorna os dados carregados do arquivo JSON como resposta JSON
    except Exception as e:
        return jsonify({'message': f'Erro ao obter os emails: {str(e)}'})  # Retorna uma resposta JSON com a mensagem de erro em caso de falha


# Habilitar o CORS usando o decorador after_request
@api_bp.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE"

    if response.headers.get("Content-Type") == "application/json" and response.status_code == 200:
        response.headers["Access-Control-Allow-Origin"] = "*"  # Permitir de qualquer origem para solicitações com status 200

    return response


# Tratar as solicitações de pré-voo OPTIONS explicitamente
@api_bp.route('/api/salvar-json', methods=['POST'])
def handle_post_request():
    # Lógica para manipular a solicitação POST
    salvar_arquivo_json()  # Chama a função salvar_arquivo_json para salvar o arquivo
    response = jsonify({"message": "Sucesso"})
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def salvar_arquivo_json():
    # Obter os dados JSON da solicitação
    data = request.get_json()

    # Extrair as informações relevantes do JSON
    file_path = data.get('filePath')
    data_str = data.get('dataStr')

    # Verificar se as informações estão presentes
    if file_path and data_str:
        try:
            # Salvar o arquivo no diretório temporário do sistema
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, file_path)  # Combinar o diretório temporário com o caminho fornecido

            with open(file_path, 'w') as file:
                file.write(data_str)
            print("Arquivo salvo:", file_path)  # Declaração print para verificar se o arquivo foi salvo

            return jsonify({'message': 'Arquivo salvo com sucesso!'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Informações insuficientes'}), 400
