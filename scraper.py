from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

urls = [
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

url = urls[0]
base_url = 'https://www.magazineluiza.com.br'

r = requests.get(url).content
soup = BeautifulSoup(r, 'html.parser')
subs = soup.find_all(attrs={"data-filter-type": "subcategories"})
#Navigate subcategories
sub_urls = []
for s in subs[:2]:
    href = s.find('a')['href']
    sub_urls.append(base_url + href)
    print(s.find('a')['href'])

final_product_urls = []
for u in sub_urls:
    rs = requests.get(u).content
    ssoup = BeautifulSoup(rs, 'html.parser')
    product_urls = ssoup.find_all('a', attrs={'name': 'linkToProduct'})
    for p in product_urls:
        final_product_urls.append(p['href'])


print(final_product_urls)
print(len(final_product_urls))
