from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from datetime import datetime
import pandas as pd
import json
import time
import pickle

category_urls = [
    'https://www.magazineluiza.com.br/acessorios-de-tecnologia/l/ia/',
    'https://www.magazineluiza.com.br/ar-e-ventilacao/l/ar/',
    'https://www.magazineluiza.com.br/artigos-para-festa/l/af/',
    'https://www.magazineluiza.com.br/audio/l/ea/',
    'https://www.magazineluiza.com.br/automotivo/l/au/',
    'https://www.magazineluiza.com.br/bebe/l/bb/',
    'https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/',
    'https://www.magazineluiza.com.br/brinquedos/l/br/',
    'https://www.magazineluiza.com.br/cama-mesa-e-banho/l/cm/',
    'https://www.magazineluiza.com.br/cameras-e-drones/l/cf/',
    'https://www.magazineluiza.com.br/casa-e-construcao/l/cj/',
    'https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/',
    'https://www.magazineluiza.com.br/comercio-e-industria/l/pi/',
    'https://www.magazineluiza.com.br/decoracao/l/de/',
    'https://www.magazineluiza.com.br/eletroportateis/l/ep/',
    'https://www.magazineluiza.com.br/esporte-e-lazer/l/es/',
    'https://www.magazineluiza.com.br/ferramentas/l/fs/',
    'https://www.magazineluiza.com.br/filmes-e-series/l/fm/',
    'https://www.magazineluiza.com.br/games/l/ga/',
    'https://www.magazineluiza.com.br/informatica/l/in/',
    'https://www.magazineluiza.com.br/livros/l/li/',
    'https://www.magazineluiza.com.br/mercado/l/me/',
    'https://www.magazineluiza.com.br/moda-e-acessorios/l/md/',
    'https://www.magazineluiza.com.br/musica-e-shows/l/ms/',
    'https://www.magazineluiza.com.br/natal/l/na/',
    'https://www.magazineluiza.com.br/papelaria/l/pa/',
    'https://www.magazineluiza.com.br/pet-shop/l/pe/',
    'https://www.magazineluiza.com.br/relogios/l/re/',
    'https://www.magazineluiza.com.br/suplementos-alimentares/l/sa/',
    'https://www.magazineluiza.com.br/tablets-ipads-e-e-reader/l/tb/',
    'https://www.magazineluiza.com.br/telefonia-fixa/l/tf/',
    'https://www.magazineluiza.com.br/tv-e-video/l/et/',
    'https://www.magazineluiza.com.br/utilidades-domesticas/l/ud/'
]

base_url = 'https://www.magazineluiza.com.br'
s = requests.Session()
results = []
now = datetime.now()
for category_url in category_urls:
    then = datetime.now()
    cat_name = category_url.split('/')[3]
    print(then, cat_name)
    # Handle expired session
    try:
        r = s.get(category_url).content
    except:
        retries = 0
        while retries < 3:
            try:
                s = requests.Session()
                r = s.get(category_url).content
                break
            except:
                time.sleep(300)
            retries += 1


    # Find subcategories
    soup = BeautifulSoup(r, 'html.parser')
    subs = soup.find_all(attrs={"data-filter-type": "subcategories"})
    # Navigate subcategories
    #sub_urls = []
    for s in subs:
        subcat_alias = s['data-filter-value']
        tmp = s.find('a')
        href = tmp['href']
        # sub_urls.append([category_url, base_url + href])
        url = base_url + href
        subcat_name = tmp.text
        print('New Sub: ', subcat_name)
        # print(subcat_name)
        sub_req = None
        try:
            sub_req = s.get(url).content
        except:
            retries = 0
            while retries < 3:
                try:
                    s = requests.Session()
                    sub_req = s.get(url).content
                    break
                except:
                    time.sleep(300)
                retries += 1
        subcat_soup = BeautifulSoup(sub_req, 'html.parser')
        last_page = int(subcat_soup.find_all(attrs={'class': 'css-1a9p55p'})[-2].text)
        results.append([url, last_page])

then = datetime.now()
print('tempo: ', (then-now).seconds)
with open('results', 'wb') as f:
    pickle.dump(results, f)
