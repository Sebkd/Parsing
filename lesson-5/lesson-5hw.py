'''
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (
от кого - from_post
дата отправки -data
тема письма,
текст письма полный
)
Логин тестового ящика: stu*****@mail.ru
Пароль тестового ящика: *********
'''
import hashlib
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time

from secret import LOGIN_MAIL, PASSWORD_MAIL


def insert_db(dictionary, db_base, hash_link):
    '''Функция по заполнению базы данных'''
    for dict_v in dictionary.values():
        try:
            db_base.insert_one({
                # _id заполняется посредством hash из ссылки, которая уникальна
                # проверку hash делаем именно на этом этапе, так как база данных по идеи будет дополняться
                # и делать проверку на более раннем этапе нецелесообразно, так как там просто делается словарь объектов
                '_id': (hashlib.sha256(dict_v[hash_link].encode())).hexdigest(),
                '_data': dict_v,
            })
        except DuplicateKeyError:
            print('есть такой элемент')
            continue


def parsing_mail_links():
    hrefs = set()
    check = 0
    while True:
        mail_links = driver.find_elements(By.XPATH,
                                          '//a[contains(@class, "llct llct_new '
                                          'llct_new-selection js-letter-list-item")]')
        for mail_link in mail_links:
            hrefs.add(mail_link.get_attribute('href'))

        if len(hrefs) == check:
            return hrefs

        check = len(hrefs)
        actions = ActionChains(driver)  # накапливает события как стек
        actions.move_to_element(mail_links[-1])
        actions.perform()
        time.sleep(1)


def parsing_mail(data_from_emails, hrefs, *args):
    xpath_get_from_email, xpath_get_date_email, xpath_get_subject_email, xpath_get_body_email = args

    for index, href in enumerate(hrefs):
        item_dict = {}

        driver.get(href)
        # get from_email
        elem = driver.find_element(By.XPATH, xpath_get_from_email)
        from_email = elem.get_attribute('title')

        # date_email
        elem = driver.find_element(By.XPATH, xpath_get_date_email)
        date_email = elem.text

        # subject_email
        elem = driver.find_element(By.XPATH, xpath_get_subject_email)
        subject_email = elem.text

        # body_email
        elem = driver.find_element(By.XPATH, xpath_get_body_email)
        body_email = elem.get_attribute('outerHTML')

        item_dict['href'] = href
        item_dict['from_email'] = from_email
        item_dict['date_email'] = date_email
        item_dict['subject_email'] = subject_email
        item_dict['body_email'] = body_email

        data_from_emails[index] = item_dict.copy()
    return data_from_emails


if __name__ == "__main__":
    service = Service('./chromedriver')

    chrome_options = Options()  # для работы с опциями браузера, например чтобы он открылся на полный экран
    chrome_options.add_argument('start-maximized')  # полный экран
    # ua='cat'
    # chrome_options.add_argument('--user-agent=%s' % ua)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    driver.get('https://mail.ru/')

    button = driver.find_element(By.XPATH, '//button[contains(text(), "Войти")]')
    button.click()

    # не победил iframe во всплывающем окне, поэтому открываю в новой вкладке
    input_frame = driver.find_element(By.CLASS_NAME, 'ag_js-popup-frame')
    link = input_frame.find_element(By.XPATH, "//iframe[contains(@class, 'ag-popup__frame__layout__iframe')]")
    driver.get(link.get_attribute('src'))

    # login
    elem = driver.find_element(By.XPATH, '//input[contains(@name, "username")]')
    elem.send_keys(LOGIN_MAIL)
    elem.send_keys(Keys.ENTER)

    # password
    elem = driver.find_element(By.XPATH, '//input[contains(@name, "password")]')
    elem.send_keys(PASSWORD_MAIL)
    elem.send_keys(Keys.ENTER)

    hrefs = parsing_mail_links()

    XPATH_FROM_EMAIL = '//span[contains(@class, "letter-contact")]'
    XPATH_DATE_EMAIL = '//div[contains(@class, "letter__date")]'
    XPATH_SUBJECT_EMAIL = '//h2[contains(@class, "thread-subject")]'
    XPATH_BODY_EMAIL = '//div[@class="letter-body"]'

    items_dict = {}

    items_dict = parsing_mail(items_dict,
                              hrefs,
                              XPATH_FROM_EMAIL,
                              XPATH_DATE_EMAIL,
                              XPATH_SUBJECT_EMAIL,
                              XPATH_BODY_EMAIL)

    driver.close()
    driver.quit()

    client = MongoClient('localhost', 27017)

    db_mongo = client['emails']
    db_mongo.drop_collection('emails')  # для полноценного стирания базы данных
    emails = db_mongo.emails
    hash_link = 'href'

    insert_db(items_dict, emails, hash_link)
