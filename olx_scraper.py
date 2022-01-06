#!/usr/bin/env python3

from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import time
import datetime

engine = create_engine('mysql+pymysql://root:pass@/scrapper', encoding='UTF-8', echo=False)
rooms = {'rooms': ['one', 'two', 'three', 'four']}
market = {'market': ['primary', 'secondary']}
dictionary = {}
title = []
price = []
offer_type = []
price_per_meter = []
floor = []
area = []
type_of_building = []
city_list = []
market_list = []
rooms_list = []
no_page_found = []
scrap_month = []
scrap_year = []
voivodeship_list = []
date = datetime.datetime.now()


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


def parse_price_per_meter(price):
    return float(price.replace(' ', '').replace('zł/m²', '').replace(',', '.').replace('Cenazam²:', ''))


def parse_level(level_text):
    return int(level_text.replace('Poziom: ', '').replace('Parter', '0')
               .replace('Powyżej ', '').replace('Suterena', '-1').replace('Poddasze', '11'))


def parse_area(area_text):
    return float(area_text.replace('Powierzchnia: ', '').replace(' m²', '').replace(',', '.'))


def parse_type_of_building(type_of_building_text):
    return type_of_building_text.replace('Rodzaj zabudowy: ', '')


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


def page_scrapper(soup):  # TODO add otodom BeautifulSoup
    for info in soup.findAll('div', class_='css-1wws9er'):
        try:
            title.append(info.findNext('h1', class_="css-r9zjja-Text eu5v0x0").get_text().strip())
            price.append(parse_price(info.findNext('h3', class_='css-okktvh-Text eu5v0x0').get_text().strip()))
            offer_type.append(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[0].get_text().strip())
            price_per_meter.append(
                parse_price_per_meter(info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[1].get_text().strip()))
            level_text = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[2].get_text().strip()
            if level_text.startswith('Poziom'):
                floor.append(parse_level(level_text))
            else:
                floor.append(np.nan)

            area_text = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[6].get_text().strip()
            if area_text.startswith('Powierzchnia'):
                area.append(parse_area(area_text))
            else:
                area.append(np.nan)

            type_of_building_txt = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[5].get_text().strip()
            if type_of_building_txt.startswith('Rodzaj'):
                type_of_building.append(parse_type_of_building(type_of_building_txt))
            else:
                type_of_building.append(np.nan)

            city_list.append(city)
            market_list.append(market.replace('secondary', 'wtorny').replace('primary', 'pierwotny'))
            rooms_list.append(
                int(room.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4')))
            scrap_month.append(date.strftime('%B'))
            scrap_year.append(date.strftime('%Y'))
            index = cities[cities['city'] == city].index.values
            voivodeship_list.append(cities.at[index[0], 'voivodeship'])
        except ValueError as e:
            print(f'Value Error {e}')  # TODO add saving exception to exception_log list

    dictionary = {'offer_title': title, 'price': price, 'price_per_meter': price_per_meter,
                  'offer_type': offer_type, 'floor': floor, 'area': area, 'rooms': rooms_list,
                  'offer_type_of_building': type_of_building, 'market': market_list, 'city_name': city_list,
                  'voivodeship': voivodeship_list, 'month': scrap_month, 'year': scrap_year}

    return dictionary


def offer_iterator(link_list):
    try:
        for link in range(len(link_list)):
            soup = fetch_page(link_list[link]['href'])
            result = page_scrapper(soup)
        return result
    except UnboundLocalError:
        no_page_found.append(URL)


def main(URL):
    # print(f'\nApplication starts scraping from {URL}')
    for offers_site in (range(site_pages_count(URL))):
        offer_link = offer_link_finder(URL, offers_site)
        diction = offer_iterator(offer_link)
    # print("Scrapped!!\n")
    return diction


if __name__ == '__main__':
    print('Scrapper Running...')
    exec(open('city_names_scrapper.py').read())
    start_time = time.time()
    cities = pd.read_csv('cities.csv')
    count = 0
    for i, market in enumerate(market['market']):
        for j, room in enumerate(rooms['rooms']):
            print(f'\nScraping {count + 1}/8 | market: {market} | rooms: {room}')
            for k, city in enumerate(tqdm(cities['city'])):
                URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/' + city + '/?search%5Bfilter' \
                                                                                       '_enum_market%5D%5B0%5D=' + market + '&search%5Bfilter_enum_rooms%5D%5B0%5D=' + room
                if site_pages_count(URL) is None:
                    # print(f'No offers: {URL}')
                    continue
                else:
                    df = pd.DataFrame(main(URL))
    df.drop_duplicates()
    df.to_sql('Offers', engine, if_exists='replace', index=False)
    df.to_csv('apartments.csv', mode='w', index=False)  # TODO Choice saving to DB or .csv
    pd.DataFrame(no_page_found).to_csv('no_page_found.csv', mode='w', index=False)
    print('WORK DONE!')
    print('-----%s-----' % str(datetime.timedelta(seconds=(time.time() - start_time))))
