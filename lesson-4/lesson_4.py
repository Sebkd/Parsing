import re
from pprint import pprint
import requests
from lxml import html


def parsing_mailnews(container, news_xpath, link_source_xpath, item_list):
    for item in container:
        item_dict = {}
        news = item.xpath(news_xpath)
        link_source = item.xpath(link_source_xpath)
        for index, href_source_piece in enumerate(link_source):
            response_piece = requests.get(href_source_piece, headers=headers)
            dom_source = html.fromstring(response_piece.text)
            href_source_number = re.search(r'\d{4,}', href_source_piece).group(0)
            source = dom_source.xpath(
                "//div[contains(@data-news-id, href_piece_int)]//a[contains(@class, 'link color')]/@href")[0]
            date_news = dom_source.xpath(
                "//div[contains(@data-news-id, href_piece_int)]//span[contains(@class, 'note__text')]/@datetime")[0]
            date_news = re.search(r'\d{4}-\d{2}-\d{2}', date_news).group(0)

            item_dict['source'] = source
            item_dict['news'] = news[index]
            item_dict['link_news'] = link_source[index]
            item_dict['date_news'] = date_news

            try:
                item_dict['news'] = news[index].replace('\xa0', ' ')
            except IndexError:
                item_dict['news'] = ''

            items_list.append(item_dict.copy())

    return item_list

# url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=hover+h3&_sacat=0'
# url = 'https://ru.ebay.com/b/Fishing-Equipment-Supplies/1492/bn_1851047'
url_news = 'https://news.mail.ru/'
'''
Для парсинга использовать xpath. Структура данных должна
содержать:
• название источника, source
• наименование новости, news
• ссылку на новость, link_news
• дата публикации date_news
'''
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                         'Safari/537.36'}

response = requests.get(url_news, headers=headers)
dom = html.fromstring(response.text)

items_container_top = dom.xpath("//td[contains(@class, 'daynews__main')] | //td[contains(@class, 'daynews__items')]")
items_container_ul = dom.xpath("//ul[contains(@class, 'list_half')]")

items_list = []
XPATH_NEWS_TOP = ".//span[contains(@class, 'photo__title')]/text()"
XPATH_LINK_SOURCE_TOP = ".//../../@href"
XPATH_NEWS_UL = ".//li[@class='list__item']/a/text()"
XPATH_LINK_SOURCE_UL = ".//li[@class='list__item']/a/@href"

items_list = parsing_mailnews(items_container_top, XPATH_NEWS_TOP, XPATH_LINK_SOURCE_TOP, items_list)
items_list = parsing_mailnews(items_container_ul, XPATH_NEWS_UL, XPATH_LINK_SOURCE_UL, items_list)

pprint(items_list)
# href = item.xpath(".//h3[@class='s-item__title']/../@href")[0]
#     prices = item.xpath(".//span[@class='s-item__price']//text()")
#     for index, price in enumerate(prices):
#         if ' до ' in price:
#             prices[index] = str(prices[index - 1]) + str(prices[index]) + str(prices[index + 1]).replace('\xa0', '')
#             prices.pop(index + 1)
#             prices.pop(index - 1)
#         else:
#             prices[index] = str(prices[index]).replace('\xa0', '')
#         index += 1
#     info = item.xpath(".//span[contains(@class, 's-item__hotness')]/span/text()")
#     item_dict['name'] = names
#     item_dict['href'] = href
#     item_dict['price'] = prices[0]
#     try:
#         item_dict['info'] = info[0].replace('\xa0', '')
#     except IndexError:
#         item_dict['info'] = ''
#
#     items_list.append(item_dict)
#
# pprint(items_list)
