#!/usr/bin/env python3
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
from sqlalchemy import create_engine
import pandas as pd
import time

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/'
dictionary = {}
title = []
price = []
offer_type = []
price_per_meter = []
level = []
area = []
plot_area = []
type_of_building = []
link = []


def progress_bar(progress):
    for i in tqdm(range(progress)):
        time.sleep(0.02)


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', ''))


def parse_price_per_meter(price):
    return float(price.replace(' ', '').replace('zł/m²', '').replace(',', '.').replace('Cenazam²:', ''))


def site_pages_count():
    page = get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return int(soup.findAll('span', class_='item fleft')[-1].get_text())


def offer_link_finder(number):
    page = get(f'{URL}?page={number}')
    soup = BeautifulSoup(page.content, 'html.parser')
    link_list = []
    print(f'\nScrapping page {number + 1} / {site_pages_count()}')
    for offer in soup.findAll('div', class_='offer-wrapper'):
        link = offer.findNext('a')
        link_list.append(link)
    return link_list


def page_scrapper(soup):
    for info in soup.findAll('div', class_='css-1wws9er'):
        try:
            title.append(info.findNext('h1', class_="css-r9zjja-Text eu5v0x0").get_text().strip())
            price.append(parse_price(info.findNext('h3', class_='css-okktvh-Text eu5v0x0').get_text().strip()))
            offer_type.append(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[0].get_text().strip())
            price_per_meter.append(
                parse_price_per_meter(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[1].get_text().strip()))
            level.append(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[2].get_text().strip())
            area.append(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[6].get_text().strip())
            type_of_building.append(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[5].get_text().strip())
        except ValueError as e:
            print(f'Value Error {e}')

    # print(title, price, offer_type, price_per_meter, level, area, type_of_building)

    dictionary = {'offer_title': title, 'price': price, 'offer_type': offer_type,
                  'price_per_meter': price_per_meter, 'level': level, 'area': area,
                  'offer_type_of_building': type_of_building}

    return dictionary


def parse_offer_page(link_list):
    for i in range(len(link_list)):
        site = get(link_list[i]['href'])
        soup = BeautifulSoup(site.content, 'html.parser')
        a = page_scrapper(soup)
    return a


def main():
    start_time = time.time()
    for j in range(site_pages_count()):
        offer_link = offer_link_finder(j)
        diction = parse_offer_page(offer_link)
    df = pd.DataFrame(diction)
    df['offer_title'].unique()
    df.to_csv('title.csv')
    print('-----%s seconds-----' % (time.time() - start_time))


if __name__ == '__main__':
    main()
