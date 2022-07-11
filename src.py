from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

from time import sleep

url = "https://www.airbnb.com.br/"

navegador = webdriver.Edge("Driver/msedgedriver.exe")
site = navegador.get(url)
sleep(4)

# Localizando o botao para selecionar o local
botao_local = navegador.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div/header/div/div[2]/div/div/div/div[1]/div/button[1]")
botao_local.click()
sleep(1)

# Ativando seleção pelo calendario
input_local = navegador.find_element(By.XPATH, '//*[@id="bigsearch-query-location-input"]')
input_local.send_keys("São Paulo")
# Selecionando data 1
input_data = navegador.find_element(By.XPATH, '//*[@id="search-tabpanel"]/div/div[3]/div[1]/div/div')
input_data.click()

data_inicio_pesquisa = "2022-07-22"
data_inicio = navegador.find_element(By.XPATH, f"//div[@data-testid='datepicker-day-{data_inicio_pesquisa}']")
data_inicio.click()
# Selecionando data 2
data_fim_pesquisa = "2022-07-25"
data_fim = navegador.find_element(By.XPATH, f"//div[@data-testid='datepicker-day-{data_fim_pesquisa}']")
data_fim.click()

# Buscar
botao_buscar = navegador.find_element(By.XPATH, '//*[@id="search-tabpanel"]/div/div[5]/div[2]/button') 
botao_buscar.click()

# Div das informações da hospedagem
informacoes_hospedagens = []

for pagina in range(3):
    sleep(3.5)
    pagina_atual = BeautifulSoup(navegador.page_source)
    classe_div = "cy5jw6o"
    hospedagens = pagina_atual.find_all("div", attrs={"class": classe_div})
    
    for hospedagem in hospedagens:
        # Obtendo o link da hospedagem
        classe_link = "ln2bl2p"
        link = hospedagem.find("a", attrs={"class": classe_link})["href"]
        link = "www.airbnb.com.br" + link

        # Obtendo título
        classe_titulo = "t1jojoys"
        titulo = hospedagem.find("div", attrs={"class": classe_titulo}).text

        # Obtendo Valor
        classe_valor = "_tyxjp1"
        valor = hospedagem.find("span", attrs={"class": classe_valor}).text

        informacoes_hospedagens.append([titulo, link, valor])

    botao_mudar_pagina = navegador.find_element(By.CLASS_NAME, "_1bfat5l")
    botao_mudar_pagina.click()

informacoes_hospedagens = pd.DataFrame(informacoes_hospedagens, columns=["Título", "link", "Valor"])
informacoes_hospedagens.to_excel("informacoes_hospedagens.xlsx", index=False)