import pandas as pd
import numpy as np
import requests as r
from datetime import datetime
from datetime import timezone
import json
import time
import asyncio
import aiohttp
import os
import pickle
from bs4 import BeautifulSoup
import os

async def get_product_info(product_url, session, cat_name, subcat_name):
    prod_resp = await session.get(product_url)
    prod_text = await prod_resp.read()
    prod_req = BeautifulSoup(prod_text, 'html.parser')
    try:
        p = json.loads(prod_req.find(attrs={'class': 'header-product js-header-product'})['data-product'])
        seller = prod_req.find('button', 'seller-info-button js-seller-modal-button')
        now = datetime.now()
        date = now.date()
        # Product info
        sku = p['sku']
        product_id = p['id_product']
        full_title = p['fullTitle']
        path = p['variationPath']
        quantity_sellers = p['quantitySellers']
        category_id = p['categoryId']
        subcategory = p['urlSubcategories']
        best_price = p['bestPriceTemplate']
        installment_quantity = p['installmentQuantity']
        buy_together_image = p['buyTogetherImage']
        thumbnail = p['thumbailBuyTogether']
        list_price = p['listPrice']
        installment_amount = p['installmentAmount']
        price_template = p['priceTemplate']
        p_seller = p['seller']
        # Company info
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
        #print(now, date, nome_fantasia,
        #                razao_social, cnpj, seller_url, city, state, street, number, neighborhood, cep,
        #                sku, product_id, full_title, path, quantity_sellers, category_id, subcategory,
        #                best_price, installment_quantity, buy_together_image, thumbnail, list_price,
        #                installment_amount, price_template, p_seller)
        results = [now, date, cat_name, subcat_name, nome_fantasia,
                        razao_social, cnpj, seller_url, city, state, street, number, neighborhood, cep,
                        sku, product_id, full_title, path, quantity_sellers, category_id, subcategory,
                        best_price, installment_quantity, buy_together_image, thumbnail, list_price,
                        installment_amount, price_template, p_seller
                        ]
        name = cat_name + '_' + subcat_name + '_' + sku
        with open(name, 'wb') as f:
            pickle.dump(results, f)
    except:
        print('Failed: ', product_url)
        with open('fails', 'r+b') as f:
            pickle.dump(product_url, f)


async def get_subcat_page(url, session, cat_name, subcat_name):
    async with semaphore:
        resp = await session.get(url=url)
        text = await resp.read()
        subcat_soup = BeautifulSoup(text, 'html.parser')
        if resp.status == 429:
            print('429')
            retry_after = resp.headers['Retry-After']
            await asyncio.sleep(retry_after)
            resp = await session.get(url=url)
            text = await resp.read()
            subcat_soup = BeautifulSoup(text, 'html.parser')
        main_products_list = subcat_soup.find('ul', attrs={'role': 'main'})
        main_products = [x['href'] for x in main_products_list.find_all(attrs={'name': 'linkToProduct'})]
        tasks = []
        for product_url in main_products:
            print(product_url)
            tasks.append(get_product_info(session=session, product_url=product_url, cat_name=cat_name, subcat_name=subcat_name))
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


async def main(urls):
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(get_subcat_page(session=session, url=url[0], cat_name=url[1], subcat_name=url[2]))
        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls

if __name__ == '__main__':
    with open('results', 'rb') as f:
        initial_urls = pickle.load(f)
    page_urls = []
    #print(initial_urls)
    for item in initial_urls:
        last_page = item[1]
        subcat_url = item[0]
        cat_name = item[2]
        subcat_name = item[3]
        pages = list(range(1, last_page + 1))
        for page in pages:
            page_urls.append([subcat_url + f'?page={page}', cat_name, subcat_name])
    # Page urls - OK
    print(len(page_urls))
    now = datetime.now()
    print(now)
    os.chdir('data')
    semaphore = asyncio.Semaphore(32)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(page_urls))
    then = datetime.now()
    print(then)