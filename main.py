from flask import Flask, jsonify
import os
from datetime import datetime, timedelta

BASE_PATH = r'D:\gStorage\RECORD_FILE'

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

@app.route("/gravacoes", methods=["GET"])
def gravacoes():
    return jsonify(get_gravacao())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
