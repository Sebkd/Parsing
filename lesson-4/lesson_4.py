from pprint import pprint
import requests
from lxml import html

# url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=hover+h3&_sacat=0'
url = 'https://ru.ebay.com/b/Fishing-Equipment-Supplies/1492/bn_1851047'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                         'Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

items_container = dom.xpath("//li[contains(@class, 's-item')]")
# for yandex news //a[contains(@class, 'mg-card__link')]
items_list = []
for item in items_container:
    item_dict = {}
    names = item.xpath(".//h3[@class='s-item__title']/text()")[0]
    href = item.xpath(".//h3[@class='s-item__title']/../@href")[0]
    prices = item.xpath(".//span[@class='s-item__price']//text()")
    for index, price in enumerate(prices):
        if ' до ' in price:
            prices[index] = str(prices[index - 1]) + str(prices[index]) + str(prices[index + 1]).replace('\xa0', '')
            prices.pop(index + 1)
            prices.pop(index - 1)
        else:
            prices[index] = str(prices[index]).replace('\xa0', '')
        index += 1
    info = item.xpath(".//span[contains(@class, 's-item__hotness')]/span/text()")
    item_dict['name'] = names
    item_dict['href'] = href
    item_dict['price'] = prices[0]
    try:
        item_dict['info'] = info[0].replace('\xa0', '')
    except IndexError:
        item_dict['info'] = ''

    items_list.append(item_dict)

pprint(items_list)

