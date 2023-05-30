from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_SENDER = 'botemail3040@gmail.com'
EMAIL_PASSWORD = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    destinatario = request.form.get('destinatario')
    assunto = request.form.get('assunto')
    corpo = request.form.get('corpo')

    if enviar_email(destinatario, assunto, corpo):
        return render_template('result.html', message='Mensagem enviada com sucesso!')
    else:
        return render_template('result.html', message='Erro ao enviar mensagem.')

def enviar_email(destinatario, assunto, corpo):
    try:
        mensagem = MIMEMultipart()
        mensagem['From'] = EMAIL_SENDER
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto

        mensagem.attach(MIMEText(corpo, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            servidor.send_message(mensagem)

        return True
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')
        return False

if __name__ == '__main__':
    app.run(port=5500, debug=True)
