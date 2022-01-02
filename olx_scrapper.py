#!/usr/bin/env python3

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
from sqlalchemy import create_engine
import pandas as pd
import time

engine = create_engine('mysql+pymysql://root:zddatapol17@/scrapper', encoding='UTF-8', echo=False)
dictionary = {}
title = []
price = []
offer_type = []
price_per_meter = []
level = []
area = []
type_of_building = []
city_list = []


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', ''))


def parse_price_per_meter(price):
    return float(price.replace(' ', '').replace('zł/m²', '').replace(',', '.').replace('Cenazam²:', ''))


def setup(argv):
    pass  # TODO


def fetch_page(URL):
    page = get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def site_pages_count(URL):
    soup = fetch_page(URL)
    result = soup.findAll('span', class_='item fleft')
    if len(result) > 0:
        result = int(result[-1].get_text())
    elif len(soup.findAll('h1', class_='c41 lheight24')) > 0:
        return None
    else:
        result = 1
    return result


def offer_link_finder(URL, number):
    soup = fetch_page(f'{URL}&page={number}')
    link_list = []
    for offer in soup.findAll('div', class_='offer-wrapper'):
        link = offer.findNext('a')
        link_list.append(link)
    return link_list


def page_scrapper(soup):  # TODO add city name from URL
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
            city_list.append(city)
        except ValueError as e:
            print(f'Value Error {e}')

    dictionary = {'offer_title': title, 'price': price, 'offer_type': offer_type,
                  'price_per_meter': price_per_meter, 'level': level, 'area': area,
                  'offer_type_of_building': type_of_building, 'city_name': city_list}

    return dictionary


def offer_iterator(link_list):
    try:
        for i in range(len(link_list)):
            soup = fetch_page(link_list[i]['href'])
            result = page_scrapper(soup)
        return result
    except UnboundLocalError:
        print(f'Page not found {URL}')


def main(URL):
    print(f'\nApplication starts scraping from {URL}')
    for offers_site in tqdm(range(site_pages_count(URL))):
        offer_link = offer_link_finder(URL, offers_site)
        diction = offer_iterator(offer_link)
    print("Scrapped!!\n")
    return diction


if __name__ == '__main__':
    print('Scrapper Runing...')

    start_time = time.time()
    data = pd.read_csv('cities.csv')
    print('WORK START!!!')
    for ind, city in enumerate(data['0']):
        URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/' + city + '/?search%5Bfilter_enum_market%5D%5B0%5D=' \
                                                                               'secondary&search%5Bfilter_enum_rooms%5D%5B0%5D=two'
        if site_pages_count(URL) is None:
            print(f'No offers: {URL}')
        else:
            df = pd.DataFrame(main(URL))

    df.to_sql('Offers', engine, if_exists='append', index=False)  # TODO Saving wrong cities .csv is ok
    df.to_csv('apartments.csv', mode='a', index=False)  # TODO Choice saving to DB or .csv

    print('WORK DONE!')
    print('-----%s seconds-----' % (time.time() - start_time))
