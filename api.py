import pandas as pd
from flask import Flask

app = Flask(__name__)

hospedagens = pd.read_json("data/informacoes_hospedagens.json", orient="index")

@app.route("/", methods=["GET", "POST"])
def mensagem_inicio():
    return hospedagens.to_json(orient="index")

app.run()
