from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from tqdm import tqdm

print('Creating cities.csv file...')
path = 'voivodeship.csv'
data = pd.read_csv(path, index_col=0)
city_name = []


def fetch_page(URL):
    page = get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def parse_city_name(name):
    return str(name.replace(' ', '-').replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l') \
               .replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ż', 'z').replace('ź', 'z').replace('""',
                                                                                                                  ''))


for index, URL in tqdm(enumerate(data['links'])):
    soup = fetch_page(URL)
    for info in soup.findAll('span', class_='link'):
        city_name.append(parse_city_name(info.findAllNext('a', class_='tdnone')[0].get_text().strip().lower()))
    city_name.pop()

file = pd.DataFrame(city_name)
file.to_csv('cities.csv', mode='w', index=False)
