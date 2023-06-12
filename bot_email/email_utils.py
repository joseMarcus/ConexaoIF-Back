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
        json_content = file.read()
        data = json.loads(json_content)
        return data

def enviar_email(assunto, mensagem_manual):
    try:
        emails_data = load_json_from_file(file_path)
        emails = emails_data['emails']

        for email_data in emails:
            assunto_email = email_data['titulo']
            corpo = f"{email_data['link']}\n\n{mensagem_manual}"

            mensagem = MIMEMultipart()
            mensagem['From'] = EMAIL_SENDER
            mensagem['To'] = email_data['email']
            mensagem['Subject'] = assunto_email
            mensagem.attach(MIMEText(corpo, 'plain'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
                servidor.starttls()
                servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
                servidor.send_message(mensagem)

        return True
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')
        return False

def load_emails():
    try:
        file = request.files['arquivo']
        file_path = os.path.join(file.filename)
        file.save(file_path)

        emails_data = load_json_from_file(file_path)
        emails = emails_data['emails']

        first_group = emails[0]  # Considerando apenas o primeiro grupo do arquivo
        titulo_grupo = first_group['titulo']
        link_grupo = first_group['link']

        return jsonify({'message': 'Arquivo carregado com sucesso!', 'titulo_grupo': titulo_grupo, 'link_grupo': link_grupo})
    except Exception as e:
        return jsonify({'message': f'Erro ao carregar arquivo: {str(e)}'})
