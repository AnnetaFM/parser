import requests
from bs4 import BeautifulSoup
import csv


CSV = 'condos.csv'
HOST = 'https://www.dotproperty.co.th/en'
URL = 'https://www.dotproperty.co.th/en/condos-for-rent/prachuap-khiri-khan'
HEADERS = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(
        'div',
        class_='search-list featured property-snippet-updated'
    )
    condos = []

    for item in items:
        condos.append(
            {
                'name': item.find('h3', class_='name').get_text(strip=True),
                'price': item.find('div', class_='price').get_text(strip=True),
                'photo': item.find('div', class_='gallery btn-js-link').find('img').get('src'),
                'link': item.find('div', class_='description-block').find('a').get('href')
            }
        )
    return condos


def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Имя', 'Цена', 'Фото', 'Ссылка'])
        for item in items:
            writer.writerow([
                item['name'],
                item['price'],
                item['photo'],
                item['link'],
            ])
        print(f'Результаты сохранены в файле {path}')


def parser():
    PAGINATION = input('Укажите количество страниц для парсинга: ')
    PAGINATION = int(PAGINATION.strip())
    condos = []
    for page in range(1, PAGINATION+1):
        print(f'Парсим страницу: {page}')
        html = get_html(URL, params={'page': page})
        if html.status_code == 200:
            page_condos = get_content(html.text)
            condos.extend(page_condos)
        else:
            print(f'Ошибка при получении страницы {page}')
    if condos:
        save_doc(condos, CSV)
    else:
        print('Error')


parser()
