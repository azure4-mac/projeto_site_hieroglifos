import os
from dotenv import load_dotenv
import psycopg
from flask import Flask, render_template, jsonify, redirect, url_for

# Carregar variáveis de ambiente
load_dotenv()

# Conectar ao banco de dados PostgreSQL
connection_db = psycopg.connect(
    "dbname=amnipora user=postgres password=3f@db host=164.90.152.205 port=80"
)

app = Flask(__name__, static_folder='../FrontEnd/static', template_folder='../FrontEnd/templates')

@app.route('/')
def index():
    return render_template('index.html')  # Carrega o index.html ao acessar a raiz

@app.route('/sinais')
def sinais():
    return render_template('sinais.html')  # Página de hieróglifos

@app.route('/api/hieroglyphs', methods=['GET'])
def get_hieroglyphs():
    with connection_db.cursor() as cursor:
        cursor.execute("SELECT symbol, gardiner, unicode_code, description FROM hieroglifo")
        hieroglyphs = cursor.fetchall()
        
        result = [{
            'symbol': h[0],
            'gardiner': h[1],
            'unicode_code': h[2],
            'description': h[3]
        } for h in hieroglyphs]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
