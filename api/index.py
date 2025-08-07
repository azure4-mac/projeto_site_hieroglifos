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


from openai import OpenAI
from flask import request
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route('/api/traduzir', methods=['GET'])
def traduzir():
    texto_pt = request.args.get("texto", "").strip()
    if not texto_pt:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um tradutor de português para inglês. Responda somente com a tradução direta."},
                {"role": "user", "content": texto_pt}
            ],
            max_tokens=200
        )
        texto_en = response.choices[0].message.content.strip()
        print(f"Texto traduzido: {texto_en}")

        stopwords = {"the", "a", "an", "of", "in", "on", "and", "to", "is", "are", "for", "with"}
        palavras = [p for p in re.findall(r'\b\w+\b', texto_en.lower()) if p not in stopwords]
        print(f"Palavras extraídas: {palavras}")

        simbolos = []
        traduzidos = set()

        with connection_db.cursor() as cursor:
            for palavra in palavras:
                if palavra in traduzidos:
                    continue
                traduzidos.add(palavra)

                cursor.execute(
                    "SELECT symbol FROM hieroglifo WHERE LOWER(description) LIKE %s LIMIT 1",(f"%{palavra}%",))
                res = cursor.fetchone()
                print(f"Busca pela palavra '{palavra}': {res}")
                if res:
                    simbolos.append(res[0])

        resultado = ''.join(simbolos) if simbolos else "?"
        print(f"Resultado final (símbolos): {resultado}")

        return jsonify({'resultado': resultado})

    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({'erro': 'Erro ao processar a tradução', 'detalhe': str(e)}), 500


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run(debug=True)
