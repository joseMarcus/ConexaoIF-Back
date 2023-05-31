# Docdis

# Como rodar

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
Ctrl + C

# Cria o banco "models" com id "postgres" e senha "123" ou então modifica no arquivo "app.py"

flask db init
flask run
Ctrl + C
flask db migrate -m "Models and Resources"
flask db upgrade
flask run
