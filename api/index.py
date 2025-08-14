from dotenv import load_dotenv
import psycopg
import os
from flask import Flask, render_template, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

connection_db = psycopg.connect(os.getenv("DATABASE_URL"))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sinais')
def sinais():
    return render_template('sinais.html')

@app.route('/artigo')
def artigo():
    return render_template('artigo.html')

@app.route('/tradutor')
def tradutor():
    return render_template('tradutor.html')

@app.route('/api/hieroglyphs')
def get_hieroglyphs():
    with connection_db.cursor() as cursor:
        cursor.execute("SELECT symbol, gardiner, unicode_code, description FROM hieroglifo")
        data = cursor.fetchall()
    return jsonify([
        {
            "symbol": h[0],
            "gardiner": h[1],
            "unicode_code": h[2],
            "description": h[3]
        } for h in data
    ])


import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import io

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("A chave de API do Google não foi encontrada. Defina a variável de ambiente GOOGLE_API_KEY.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")


model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/api/traduzir_imagem', methods=['POST'])
def traduzir_imagem():
    """
    Recebe uma imagem, envia para a API do Gemini para traduzir hieróglifos
    e retorna o texto traduzido em português.
    """
    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem fornecida'}), 400

    file = request.files['imagem']

    if file.filename == '':
        return jsonify({'erro': 'Nenhum arquivo de imagem selecionado'}), 400

    try:

        image = Image.open(file.stream)

        prompt_parts = [
            "Traduza os hieróglifos egípcios desta imagem para uma mensagem clara em português, limite-se a 200 caracteres e seja direto.",
            "Se não houver hieróglifos, responda apenas 'Nenhum hieróglifo encontrado'.",
            "Já foi informado ao usuário que o contexto do texto prescisa de conhecimento especializado, não inclua essa mensagem em sua resposta.",
            image,
        ]

        print("Enviando imagem e prompt para o Gemini...")

        response = model.generate_content(prompt_parts)

        resultado_traducao = response.text.strip()
        print(f"Resposta do Gemini: {resultado_traducao}")

        return jsonify({'resultado': resultado_traducao})

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return jsonify({'erro': 'Ocorreu um erro ao processar a imagem', 'detalhe': str(e)}), 500


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run(debug=True)
