from pprint import pprint
from urllib.parse import urlencode, urljoin, quote_plus, unquote

from bs4 import BeautifulSoup
import requests

# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
#                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
#                          'Safari/537.36'}
#
# URL = 'https://www.kinopoisk.ru/lists/series-top250/?quick_filters=serials&tab=all'
#
# base_url = 'https://www.kinopoisk.ru'
# add_serial_url = '/lists/series-top250/'
# params = {
#     # 'quick_filters' : ['serials', 'films'],
#     'quick_filters': 'serials',
#     'tab' : 'all',
#         }
#
# response = requests.get(base_url + add_serial_url, headers=headers, params=params)
# print(response.url)

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                          'Safari/537.36'}

# https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=Python+%D1%81%D1%82%D0%B0%D0%B6%D0%B5%D1%80
# https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=Python+стажер

#ttps://hh.ru/search/vacancy - base_url
# clusters=true, area=1, ored_clusters=true, enable_snippets=true, salary=, text=


if __name__ == "__main__":
    # search_vacancy = str(input('Введите какую профессию будем искать или по какому тегу? '))
    search_vacancy = 'Python стажер'
    base_url = 'https://hh.ru/search/vacancy'
    params = {
        'clusters' : 'true',
        'area' : 1,
        'ored_clusters' : 'true',
        'enable_snippets' : 'true',
        'salary' : '',
        'text' : search_vacancy,
    }
    query = "?" + urlencode(params)
    url = urljoin(base_url, query)
    response = requests.get(url, headers=HEADERS)
    if response.ok:
        dom = BeautifulSoup(response.text, 'html.parser')
        quotes = dom.find_all('div', {'class': 'vacancy-serp-item'})
        dict_vacancy = {}
        for quote in quotes:
            # pprint(type(quote))
            quote_title = quote.find('a').getText()
            if quote.find('span', attrs={'data-qa' : 'vacancy-serp__vacancy-compensation'}) is None:
                quote_salary = 'None'
            else:
                quote_salary = quote.find('span', attrs={'data-qa' : 'vacancy-serp__vacancy-compensation'}).text
            print(quote_salary)
            quote_val = 0
            if len(quote_salary[:-1]) > 15:
                quote_val = quote_salary[-4:-1]
                quote_max = quote_salary.split()
                print(quote_max)

