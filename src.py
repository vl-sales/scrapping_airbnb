from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

from time import sleep

from logging import warning, error, critical
from logging import basicConfig
from logging import StreamHandler, FileHandler

# Configuração dos logs
format = '%(asctime)s - %(levelname)s- %(message)s'
handler_txt = FileHandler("logs/meus_logs.txt", "a")

basicConfig(
    format=format,
    encoding="utf-8",
    handlers=[handler_txt, StreamHandler()]
)

url = "https://www.airbnb.com.br/"

navegador = webdriver.Edge("Driver/msedgedriver.exe")
site = navegador.get(url)
sleep(4)

# Localizando o botao para selecionar o local
xpath_local = "/html/body/div[5]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div/header/div/div[2]/div/div/div/div[1]/div/button[1]"
try:
    botao_local = navegador.find_element(By.XPATH, xpath_local)
    botao_local.click()
    sleep(1)
except:
    error("Não foi possível encontrar o botão de local")

# Digitando o local
try:
    input_local = navegador.find_element(By.XPATH, '//*[@id="bigsearch-query-location-input"]')
    input_local.send_keys("São Paulo")
except:
    warning("Não foi possível localizar o input de local")

# Ativando seleção pelo calendario
# Selecionando data 1
encontrado = None
try:
    input_data = navegador.find_element(By.XPATH, '//*[@id="search-tabpanel"]/div/div[3]/div[1]/div/div')
    input_data.click()
    encontrado = 1
except:
    warning("Não foi possível localizar o input de data")

if encontrado:
    data_inicio_pesquisa = "2022-07-22"
    data_inicio = navegador.find_element(By.XPATH, f"//div[@data-testid='datepicker-day-{data_inicio_pesquisa}']")
    data_inicio.click()
    # Selecionando data 2
    data_fim_pesquisa = "2022-07-25"
    data_fim = navegador.find_element(By.XPATH, f"//div[@data-testid='datepicker-day-{data_fim_pesquisa}']")
    data_fim.click()

# Buscar
try:
    botao_buscar = navegador.find_element(By.XPATH, '//*[@id="search-tabpanel"]/div/div[5]/div[2]/button') 
    botao_buscar.click()
except:
    critical("Não foi possível localizar o botão de buscar")

# Div das informações da hospedagem
informacoes_hospedagens = []

for pagina in range(3):
    sleep(3.5)
    pagina_atual = BeautifulSoup(navegador.page_source)
    try:
        classe_div = "cy5jw6o"
        hospedagens = pagina_atual.find_all("div", attrs={"class": classe_div})
    except:
        critical("Não foi possível encontrar nenhuma hospedagem")
    
    for hospedagem in hospedagens:
        # Obtendo o link da hospedagem
        classe_link = "ln2bl2p"
        try:
            link = hospedagem.find("a", attrs={"class": classe_link})["href"]
            link = "www.airbnb.com.br" + link
        except:
            warning("Não foi possível encontrar o link da hospedagem")
            link = ""

        # Obtendo título
        classe_titulo = "t1jojoys"
        try:
            titulo = hospedagem.find("div", attrs={"class": classe_titulo}).text
        except:
            warning("Não foi possível encontrar o título da hospedagem")
            titulo = ""

        # Obtendo Valor
        classe_valor = "_tyxjp1"
        try:
            valor = hospedagem.find("span", attrs={"class": classe_valor}).text
        except:
            warning("Não foi possível encontrar o preço da hospedagem")
            valor = ""          

        informacoes_hospedagens.append([titulo, link, valor])
    
    try:
        classe_bota_mudar_pag = "_1bfat5l"
        botao_mudar_pagina = navegador.find_element(By.CLASS_NAME, classe_bota_mudar_pag)
        botao_mudar_pagina.click()
    except:
        critical("Não foi possível mudar de página")

informacoes_hospedagens = pd.DataFrame(informacoes_hospedagens, columns=["Título", "link", "Valor"])
informacoes_hospedagens.to_excel("informacoes_hospedagens.xlsx", index=False)