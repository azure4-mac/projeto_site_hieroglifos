import os
from dotenv import load_dotenv
import psycopg
from flask import Flask, render_template, jsonify, requests

# Carregar variáveis de ambiente
load_dotenv()

connection_db = psycopg.connect(
    "dbname=mac user=postgres password=3f@db host=164.90.152.205 port=80"
)

app = Flask(__name__, static_folder='../FrontEnd/static', template_folder='../FrontEnd/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sinais')
def sinais():
    return render_template('sinais.html')

@app.route('/artigo')
def artigo():
    return render_template('artigo.html')


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

@app.route('/tradutor')
def tradutor():
    return render_template('tradutor.html')

import openai
from flask import request

FABRICIUS_API_URL = "http://localhost:8000/translate"

@app.route('/api/traduzir', methods=['GET'])
def traduzir():
    texto = request.args.get("texto", "")
    if not texto:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    gardiner_codes = [c.upper() for c in texto if c.isalpha()]  
    try:
        response = requests.post(FABRICIUS_API_URL, json={"codes": gardiner_codes})
        if response.status_code != 200:
            return jsonify({'erro': 'Erro na API do Fabricius', 'detalhe': response.text}), 500

        data = response.json()
        return jsonify({'resultado': data.get("translation", "Tradução não encontrada")})

    except Exception as e:
        return jsonify({'erro': 'Falha ao conectar com o Fabricius', 'detalhe': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
