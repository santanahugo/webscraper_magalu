from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests


url = 'https://www.magazineluiza.com.br/monitor-gamer/informatica/s/in/mogm/'
base_url = 'https://www.magazineluiza.com.br'

r = requests.get(url).content
soup = BeautifulSoup(r, 'html.parser')

main_products_list = soup.find('ul', attrs={'role':'main'})
main_products = [x['href'] for x in main_products_list.find_all(attrs={'name': 'linkToProduct'})]
for product in main_products:
    new_req = BeautifulSoup(requests.get(product).content, 'html.parser')
    seller = new_req.find('button', 'seller-info-button js-seller-modal-button')
    try:
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
        print(nome_fantasia, seller_url, city, state, razao_social, street, number, neighborhood, cnpj, cep)
    except:
        print('Vendido por Magalu')