import os
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, abort
from pyngrok import ngrok

# =========== CONFIGURAÇÕES ==============
BASE_PATH = r'D:\gStorage\RECORD_FILE' # Caminho padrão da TecnoMobile
TOKEN_API = "Mark_Kross" # Auth Token da API
PORTA_API = 5000 # Porta que a API ta rodando
TOKEN_NGROK = "não vou colocar meu token do ngrok no github nem a pau, depois do commit eu coloco" # Token do Ngrok

# ========== FLASK APP ===================
app = Flask(__name__)

def get_gravacao():
    tolerancia = datetime.now() - timedelta(days=3)
    veiculos = []

    data_mais_recente = None

    for nome in os.listdir(BASE_PATH):
        caminho = os.path.join(BASE_PATH, nome)
        if os.path.isdir(caminho):
            ult_mod = os.path.getmtime(caminho)
            data_mod = datetime.fromtimestamp(ult_mod)
            parsing = data_mod.strftime('%d/%m/%Y')

            status = "Regular" if data_mod >= tolerancia else "Atrasado"

            veiculos.append({
                "Veiculo": nome,
                "Ultima Gravação": parsing,
                "Status": status
            })

            if data_mais_recente is None or data_mod > data_mais_recente:
                data_mais_recente = data_mod

    return {
        "dados": veiculos,
        "data_mais_recente": data_mais_recente.strftime('%d/%m/%Y %H:%M:%S') if data_mais_recente else None
    }

# ============= REST API ===================

@app.before_request
def autenticar():
    token = request.headers.get("Authorization")
    if token != f"Bearer {TOKEN_API}":
        abort(401, description="Token Inválido/Faltando.")

@app.route("/gravacoes", methods=["GET"])
def gravacoes():
    return jsonify(get_gravacao())

if __name__ == "__main__":
    # Configura o Token e inicia o tunel
    ngrok.set_auth_token(TOKEN_NGROK)
    public_url = ngrok.connect(PORTA_API, "http")

    # Endpoint do Tunel
    print(f'API disponivel em: {public_url}/gravacoes')

    # Roda o server Flask
    app.run(port=PORTA_API)
