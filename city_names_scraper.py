from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from tqdm import tqdm

print('Creating cities.csv file...')
path = 'voivodeship.csv'
data = pd.read_csv(path, index_col=0)
iterator = data['links']
city_name = []
voivodeship_name = []
dictionary = {}


def fetch_page(URL):
    page = get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def parse_city_name(name):
    return str(name.replace(' ', '-').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l') \
               .replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ż', 'z').replace('ź', 'z').replace('""',
                                                                                                                  ''))


for index, URL in enumerate(tqdm(iterator)):
    soup = fetch_page(URL)
    for info in soup.findAll('span', class_='link'):
        city_name.append(parse_city_name(info.findAllNext('a', class_='tdnone')[0].get_text().strip().lower()))
        voivodeship_name.append(data.at[index, 'voivodeship'])
    city_name.pop()
    voivodeship_name.pop()
dictionary = {'city': city_name, 'voivodeship': voivodeship_name}

file = pd.DataFrame(dictionary)
file.to_csv('cities.csv', mode='w', index=True)
