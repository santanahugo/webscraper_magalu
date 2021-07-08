from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json


url = 'https://www.magazineluiza.com.br/cabo-flat-notebook-acer-aspire-4553g-dd0zq1lc000-40-pinos-bringit/p/aga495e4d4/ia/recp/'
base_url = 'https://www.magazineluiza.com.br'
s = requests.Session()
r = s.get(url).content
soup = BeautifulSoup(r, 'html.parser')
p = json.loads(soup.find(attrs={'class': 'header-product js-header-product'})['data-product'])
print(p)