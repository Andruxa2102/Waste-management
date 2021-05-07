#!/usr/bin/env python
# coding: utf-8


import requests
import json
import datetime

# Для устойчивого парсинга - взято отсюда:
# https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Сервер не любит, когда парсят - будем маскироваться

from fake_useragent import UserAgent


# LINK		часть ссылки, откуда парсим данные (вместе с link_id дает полную ссылку на страницу)
# FOLDER	папка, куда складываем напарсенное добро
# HEADERS	просто headers
# 
# link_id	хранит ссылку на следующую для парсинга страницу  
# list_of_dicts собирает все напарсенные словари для сохранения их в JSON-файл  
# counter	счетчик, чтобы знать что скрипт работает и сохранять каждые 500 объектов.

LINK = 'https://wn-api.smartro.ru/api/inventory_media_data?id='
FOLDER = '/home/user/notebooks/Work/Waste_management_API_data/containers'
HEADERS = {
    'Accept': '*/*',
    'User-Agent': UserAgent().Chrome
}

link_id = '229255'
list_of_dicts = []
counter = 0
last_image_flag = False


def json_file_to_disk(filename, json_list):
    '''Срабатывает через каждые 500 спарсенных объектов и в случае, когда передан None в ключ "next"'''
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(json_list, file, indent=4, ensure_ascii=False)


# Для устойчивого парсинга добавим повторные запросы в случае отказа сервера

session = requests.Session()
retry = Retry(connect=6, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Цикл парсинга до тех пор, пока ключ 'next' не станет None. Выдаем сообщения через каждые 50 и 500 объектов

while last_image_flag == False:
    request = requests.get(LINK + link_id, headers=HEADERS)
    page_dict = json.loads(request.text)
    
    list_of_dicts.append(page_dict['data'])
    
    if page_dict['data']['next'] is None:
        print('Парсинг завершен!')
        json_file_to_disk(FOLDER + str(counter) + '.json', list_of_dicts)
        break
    else:
        link_id = str(page_dict['data']['next'])

    counter += 1
    
    if counter % 50 == 0:
        print(f'{str(datetime.datetime.today())} : Принял строку с номером {counter}')

    if counter % 500 == 0:
        json_file_to_disk(FOLDER + str(counter) + '.json', list_of_dicts)
        print(f'Сохранены {counter} записей в папку {FOLDER} ...')
        list_of_dicts = []
