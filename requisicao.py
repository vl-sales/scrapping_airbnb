### API SIMPLES SOMENTE PARA ILUSTRACAO
import requests
import pandas as pd
import json

link = "http://127.0.0.1:5000/"

requisicao = requests.get(link)
conteudo_pag = requisicao.content

arquivo_json = json.loads(conteudo_pag)
arquivo_json = json.dumps(arquivo_json)

df_json = pd.read_json(arquivo_json, orient="index")
print(df_json.head())

