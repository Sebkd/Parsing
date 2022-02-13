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
