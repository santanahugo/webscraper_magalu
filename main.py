from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from datetime import datetime
import pandas as pd

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

for category_url in category_urls:
    cat_name = category_url.split('/')[3]
    print(cat_name)
    # Handle expired session
    try:
        r = s.get(category_url).content
    except:
        s = requests.Session()
        r = s.get(category_url).content

    # Find subcategories
    soup = BeautifulSoup(r, 'html.parser')
    subs = soup.find_all(attrs={"data-filter-type": "subcategories"})
    # Navigate subcategories
    #sub_urls = []
    for s in subs:
        tmp = s.find('a')
        href = tmp['href']
        #sub_urls.append([category_url, base_url + href])
        sub_url = base_url + href
        subcat_name = tmp.text
        try:
            sub_req = s.get(sub_url).content
        except:
            s = requests.Session()
            sub_req = s.get(sub_url).content
        subcat_soup = BeautifulSoup(sub_req, 'html.parser')
        last_page = int(soup.find_all(attrs={'class': 'css-1a9p55p'})[-2].text)
        pages = list(range(1, last_page + 1))
        current_page = 1
        j = 1
        results = []
        fails = []
        while current_page <= last_page:
            main_products_list = subcat_soup.find('ul', attrs={'role': 'main'})
            main_products = [x['href'] for x in main_products_list.find_all(attrs={'name': 'linkToProduct'})]
            for product in main_products:
                try:
                    new_req = BeautifulSoup(s.get(product).content, 'html.parser')
                except:
                    s = requests.Session()
                    new_req = BeautifulSoup(s.get(product).content, 'html.parser')
                seller = new_req.find('button', 'seller-info-button js-seller-modal-button')
                try:
                    now = datetime.now()
                    date = now.date()
                    nome_fantasia = seller['data-seller-description']
                    seller_url = seller['data-seller-page']
                    city = seller['data-seller-city']
                    state = seller['data-seller-state']
                    razao_social = seller['data-seller-razao-social']
                    street = seller['data-seller-street']
                    number = seller['data-seller-number']
                    neighborhood = seller['data-seller-neighborhood']
                    cnpj = seller['data-seller-cnpj']
                    cep = seller['data-seller-zipcode']
                    results.append([now, date, cat_name, subcat_name, current_page, nome_fantasia, razao_social, cnpj, seller_url, city, state, street, number, neighborhood, cep])
                    if len(results) >= 50:
                        #Save batch in pkl file
                        df = pd.DataFrame(results, columns = ['now','date', 'category', 'subcategory', 'page','nome_fantasia','razao_social','cnpj',
                                                              'seller_url', 'city', 'state', 'street', 'number', 'neighborhood', 'cep'])
                        df.to_pickle(f'data/{j}_{date}.pkl')
                        results = []
                        print(now, current_page, nome_fantasia, seller_url, city, state, razao_social, street, number,
                              neighborhood, cnpj, cep)
                except:
                    # Validate
                    print('Vendido por Magalu')
                    # Save urls where seller not found for post-mortem analysis
                    fails.append(product)
                    if len(fails) >= 50:
                        df_fails = pd.DataFrame(fails, columns=['product'])
                        df_fails.to_pickle(f'fails/fail_{j}_{date}.pkl')
                        fails = []
                j += 1
            # Next page
            current_page += 1
            url = f'https://www.magazineluiza.com.br/monitor-gamer/informatica/s/in/mogm/?page={current_page}'
            try:
                sub_req = s.get(url).content
            except:
                s = requests.Session()
                sub_req = s.get(url).content
            subcat_soup = BeautifulSoup(sub_req, 'html.parser')