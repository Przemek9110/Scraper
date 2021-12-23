#!/usr/bin/env python3
from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get

URL = 'https://www.olx.pl/nieruchomosci/domy/sprzedaz/'


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', ''))

def offer_link_finder(number):
    page = get(f'{URL}?page={number}')
    soup = BeautifulSoup(page.content, 'html.parser')
    for offer in soup.findAll('div', class_='offer-wrapper'):
        link = offer.findNext('a')
        print(str(link['href']))


def parse_offer_page(link):
    site = get(link['href'])
    soup = BeautifulSoup(site.content, 'html.parser')


# def parse_category_page(number):
#     global location, title, link
#     print(f'\nPracuje nad stroną {number}')
#     page = get(f'{URL}?page={number}')
#     soup = BeautifulSoup(page.content, 'html.parser')
#     for offer in soup.findAll('div', class_='offer-wrapper'):
#         footer = offer.find('td', class_='bottom-cell')
#         location = footer.find('small', class_='breadcrumb x-normal').get_text().strip().split(',')[0]
#         title = offer.findNext('strong').get_text().strip()
#         price = parse_price(offer.findNext('p', class_='price').get_text().strip())
#         link = offer.findNext('a')
#         # parse_offer_page(link)
#         # print(link['href'])
#         # print(title, location, price)

for page in range(1, 2):
    offer_link_finder(page)
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
