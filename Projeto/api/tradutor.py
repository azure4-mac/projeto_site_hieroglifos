import os
import openai
from flask import Flask, request, jsonify
import psycopg

app = Flask(__name__)

connection_db = psycopg.connect(
    "dbname=amnipora user=postgres password=3f@db host=164.90.152.205 port=80"
)

@app.route('/api/traduzir', methods=['GET'])
def traduzir():
    texto = request.args.get("texto", "")
    if not texto:
        return jsonify({'erro': 'Texto não fornecido'}), 400

    try:
        with connection_db().cursor() as cursor:
            cursor.execute("SELECT symbol, gardiner FROM hieroglifo")
            hieroglyphs = cursor.fetchall()
            mapa = {h[1][0].lower(): h[0] for h in hieroglyphs if h[1]}
    except Exception as e:
        return jsonify({'erro': 'Erro ao acessar o banco de dados', 'detalhe': str(e)}), 500

    resultado = ''.join([mapa.get(c.lower(), c) for c in texto])

    if not resultado.strip() or request.args.get("usar_gpt", "false").lower() == "true":
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Traduza o seguinte texto para hieróglifos egípcios: {texto}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Você é um tradutor de português para hieróglifos egípcios."},
                          {"role": "user", "content": prompt}],
                max_tokens=100
            )
            resultado = response.choices[0].message['content'].strip()
        except Exception as e:
            return jsonify({'erro': 'Erro ao acessar o ChatGPT', 'detalhe': str(e)}), 500

    return jsonify({'resultado': resultado})

if __name__ == "__main__":
    app.run(debug=True)
