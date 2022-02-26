from pprint import pprint
from urllib.parse import urlencode, urljoin, quote_plus, unquote

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd



HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                         'Safari/537.36'}


if __name__ == "__main__":
    # search_vacancy = str(input('Введите какую профессию будем искать или по какому тегу? '))
    search_vacancy = 'Python стажер'
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
    # dict_vacancy = {
    #     'Наименование вакансии': None,
    #     'Предлагаемая зарплата': None,
    #     'Ссылка на вакансию': None,
    #     'Работодатель': None,
    #     'Расположение': None,
    #     'Сайт, откуда собрана вакансия': base_url,
    # }
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

        if dom.find('div', attrs={'class': 'pager'}):
            params['page'] = str(index_page)
            query = "?" + urlencode(params)
            url = urljoin(base_url, query)
            index_page += 1
            if index_page > 10:
                break
            else:
                continue
        else:
            break

    frame = pd.DataFrame(dict_vacancys)
    frame.to_excel('lesson_2.xls')
    frame.to_json('lesson-2.json')
