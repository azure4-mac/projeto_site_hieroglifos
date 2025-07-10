import os
from dotenv import load_dotenv
import psycopg
from flask import Flask, render_template, jsonify, redirect, url_for

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

@app.route('/api/traduzir', methods=['GET'])
def traduzir():
    texto = request.args.get("texto", "")
    if not texto:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    with connection_db.cursor() as cursor:
        cursor.execute("SELECT symbol, gardiner FROM hieroglifo")
        hieroglyphs = cursor.fetchall()
        mapa = {h[1][0].lower(): h[0] for h in hieroglyphs if h[1]}

    resultado = ''.join([mapa.get(c.lower(), c) for c in texto])

    if not resultado.strip() or request.args.get("usar_gpt", "false").lower() == "true":
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Traduza o seguinte texto para hieróglifos egípcios: {texto}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.0-turbo",
                messages=[
                    {"role": "system", "content": "Você é um tradutor de português para hieróglifos egípcios."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            resultado = response.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({'erro': 'Erro ao acessar o ChatGPT', 'detalhe': str(e)}), 500

    return jsonify({'resultado': resultado})


if __name__ == '__main__':
    app.run(debug=True)
