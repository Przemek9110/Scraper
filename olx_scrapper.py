#!/usr/bin/env python3
from bs4 import BeautifulSoup
from requests import get
import time

URL = 'https://www.olx.pl/nieruchomosci/domy/sprzedaz/'


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', ''))


def parse_area(area):
    return float(area.replace(' ', '').replace('m²', '').replace(',', '.'))


def site_page_count():
    page = get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return int(soup.findAll('span', class_='item fleft')[-1].get_text())


def offer_link_finder(number):
    page = get(f'{URL}?page={number}')
    soup = BeautifulSoup(page.content, 'html.parser')
    link_list = []
    print(f'\nParse page {number + 1} / {site_page_count()}')
    for offer in soup.findAll('div', class_='offer-wrapper'):
        link = offer.findNext('a')
        link_list.append(link)
    return link_list


def parse_offer_page(link_list):
    for i in range(len(link_list)):
        site = get(link_list[i]['href'])
        soup = BeautifulSoup(site.content, 'html.parser')
        # print(link_list[i]['href'])
        for info in soup.findAll('div', class_='css-1wws9er'):
            title = info.findNext('h1', class_="css-r9zjja-Text eu5v0x0").get_text()
            price = info.findNext('h3', class_='css-okktvh-Text eu5v0x0').get_text()
            offer_type = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[0].get_text()
            price_per_meter = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[1].get_text()
            market = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[2].get_text()
            area = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[3].get_text()
            plot_area = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[4].get_text()
            type_of_building = info.findAllNext('p', class_='css-xl6fe0-Text eu5v0x0')[5].get_text()
            # for loc in soup.findAll('div', class_='css-1nrl4q4'):
            # city = info.find_all_next('p', class_='css-7xdcwc-Text eu5v0x0')
            # voivodeship = info.findNext('p', class_='css-xl6fe0-Text eu5v0x0').get_text()
            print(title, price, offer_type, price_per_meter, market, area, plot_area, type_of_building)


if __name__ == '__main__':
    start_time = time.time()
    for j in range(site_page_count()):
        offer_link = offer_link_finder(j)
        parse_offer_page(offer_link)
    print('-----%s seconds-----' % (time.time() - start_time))
    # parse_category_page(page)

# driver = webdriver.Chrome()
#
#
# def site_search(item):
#     driver.get('https://allegro.pl')
#     driver.maximize_window()
#     driver.find_element(By.XPATH, '//button[text()="Ok, zgadzam się"]').click()
#     driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/header/div/div/div[1]/div/form/input').click()
#     pui.typewrite(item)
#     driver.find_element(By.XPATH, '//button[text()="szukaj"]').click()
#
# def category_finder():
#     current_url = driver.current_url
#     print(current_url)
#     soup = BeautifulSoup(page.content, 'html.parser')


# if __name__ == '__main__':
#     site_search('Adrian')
#     category_finder()
