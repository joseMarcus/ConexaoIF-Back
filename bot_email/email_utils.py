import os
import json
import smtplib
from email.mime.text import MIMEText
from flask import request, jsonify
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD

# Obtenha o diretório da pasta "Downloads" do Windows
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

# Concatene o diretório de downloads com o nome do arquivo
file_path = os.path.join(downloads_dir, 'lista.json')

def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        json_content = file.read()  # Lê o conteúdo do arquivo
        data = json.loads(json_content)  # Faz o parse do conteúdo JSON
        return data

def enviar_email(assunto, mensagem_manual):
    try:
        emails_data = load_json_from_file(file_path)  # Carrega os dados do arquivo JSON
        emails = emails_data['emails']  # Obtém a lista de emails

        for email_data in emails:
            assunto_email = email_data['titulo']  # Obtém o título do email
            corpo = f"{email_data['link']}\n\n{mensagem_manual}"  # Monta o corpo do email

            mensagem = MIMEMultipart()
            mensagem['From'] = EMAIL_SENDER  # Define o remetente do email
            mensagem['To'] = email_data['email']  # Define o destinatário do email
            mensagem['Subject'] = assunto_email  # Define o assunto do email
            mensagem.attach(MIMEText(corpo, 'plain'))  # Anexa o corpo do email à mensagem

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
                servidor.starttls()  # Inicia a conexão TLS
                servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Realiza o login no servidor SMTP
                servidor.send_message(mensagem)  # Envia a mensagem de email

        return True  # Retorna True se o envio do email foi bem-sucedido
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')
        return False  # Retorna False se ocorreu algum erro ao enviar o email

def load_emails():
    try:
        file = request.files['arquivo']  # Obtém o arquivo enviado na requisição
        file_path = os.path.join(file.filename)  # Obtém o caminho completo do arquivo
        file.save(file_path)  # Salva o arquivo no sistema de arquivos

        emails_data = load_json_from_file(file_path)  # Carrega os dados do arquivo JSON
        emails = emails_data['emails']  # Obtém a lista de emails

        first_group = emails[0]  # Considerando apenas o primeiro grupo do arquivo
        titulo_grupo = first_group['titulo']  # Obtém o título do grupo
        link_grupo = first_group['link']  # Obtém o link do grupo

        return jsonify({'message': 'Arquivo carregado com sucesso!', 'titulo_grupo': titulo_grupo, 'link_grupo': link_grupo})  # Retorna uma resposta JSON com os dados carregados
    except Exception as e:
        return jsonify({'message': f'Erro ao carregar arquivo: {str(e)}'})  # Retorna uma resposta JSON com a mensagem de erro em caso de falha
