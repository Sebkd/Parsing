from pprint import pprint
import requests
from lxml import html


url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=hover+h3&_sacat=0'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                         'Safari/537.36'}

response = requests.get(url, headers=headers)
