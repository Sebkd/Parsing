from pprint import pprint
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib

client = MongoClient('localhost', 27017)

db_mongo = client['vacancy']
db_mongo.drop_collection('vacancy') # для полноценного стирания базы данных
vacancy = db_mongo.vacancy

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                         'Safari/537.36'}


def insert_db(dict_vacancys):
    '''Функция по заполнению базы данных'''
    for vacancy_dict in dict_vacancys.values():
        try:
            vacancy.insert_one({
                # _id заполняется посредством hash из ссылки, которая уникальна
                # проверку hash делаем именно на этом этапе, так как база данных по идеи будет дополняться
                # и делать проверку на более раннем этапе нецелесообразно, так как там просто делается словарь объектов
                '_id': (hashlib.sha256(vacancy_dict["Ссылка на вакансию"].encode())).hexdigest(),
                '_vacancy': vacancy_dict,
            })
        except DuplicateKeyError:
            print('есть такой элемент')
            continue


def search_sallary_db(check_salary):
    '''Написать функцию, которая производит поиск и отправляет вакансии
    с заработной платой больше введённой суммы
    (необходимо анализировать оба поля зарплаты).'''
    salary_w_condition = list(
        vacancy.find(
            {'$or': [{"_vacancy.Предлагаемая зарплата.max": {'$gte': check_salary}},
                     {"_vacancy.Предлагаемая зарплата.min": {'$gte': check_salary}}]}
        )
    )
    return salary_w_condition


if __name__ == "__main__":
    search_vacancy = 'Python разработчик'
    base_url = 'https://hh.ru/search/vacancy'
    params = {
        'clusters': 'true',
        'area': 1,
        'ored_clusters': 'true',
        'enable_snippets': 'true',
        'salary': '',
        'text': search_vacancy,
        'page': '',
        'hhtmFrom': 'vacancy_search_list',
    }
    query = "?" + urlencode(params)
    url = urljoin(base_url, query)
    dict_vacancys = {}
    index_page = 1
    index_vacancy = 1
    query = "?" + urlencode(params)
    url = urljoin(base_url, query)
    while True:
        dict_vacancy = {
            'Наименование вакансии': None,
            'Предлагаемая зарплата': None,
            'Ссылка на вакансию': None,
            'Работодатель': None,
            'Расположение': None,
            'Сайт, откуда собрана вакансия': base_url,
        }
        response = requests.get(url, headers=HEADERS)
        # check = 0
        if response.ok:
            dom = BeautifulSoup(response.text, 'html.parser')
            quotes = dom.find_all('div', {'class': 'vacancy-serp-item'})
            for quote in quotes:
                quote_title = quote.find('a').getText()
                if quote.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}) is None:
                    quote_salary = 'None'
                else:
                    quote_salary = quote.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                pattern_salary = r'(\d+\s\d+)'
                matches_salary = re.findall(pattern_salary, quote_salary.replace(' ', ''))
                matches_currency = 'руб' if 'руб' in quote_salary else 'USD' if 'USD' in quote_salary else 'None'
                dict_salary = {
                    'min': None,
                    'max': None,
                    'валюта': matches_currency,
                }
                if len(matches_salary):
                    if len(matches_salary) > 1:
                        dict_salary['min'] = int(matches_salary[0].replace('\u202f', ''))
                        dict_salary['max'] = int(matches_salary[1].replace('\u202f', ''))
                    else:
                        if 'от' in quote_salary:
                            dict_salary['min'] = int(matches_salary[0].replace('\u202f', ''))
                        else:
                            dict_salary['max'] = int(matches_salary[0].replace('\u202f', ''))

                quote_href = quote.find('a').get('href')
                quote_company = quote.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
                quote_area = quote.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text

                dict_vacancy['Наименование вакансии'] = quote_title
                dict_vacancy['Предлагаемая зарплата'] = dict_salary
                dict_vacancy['Ссылка на вакансию'] = quote_href
                dict_vacancy['Работодатель'] = quote_company
                dict_vacancy['Расположение'] = quote_area

                dict_vacancys[index_vacancy] = dict_vacancy.copy()

                index_vacancy += 1

        if dom.find('a', attrs={'data-qa': 'pager-next'}):
            params['page'] = str(index_page)
            query = "?" + urlencode(params)
            url = urljoin(base_url, query)
            index_page += 1
        else:
            break

    insert_db(dict_vacancys)  # добавляем словарь в базу данных
    pprint(search_sallary_db(150000)) # ищем по критериям
