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
from pprint import pprint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secret import LOGIN_MAIL, PASSWORD_MAIL


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
elem = elem = driver.find_element(By.XPATH, '//input[contains(@name, "password")]')
elem.send_keys(PASSWORD_MAIL)
elem.send_keys(Keys.ENTER)

hrefs = parsing_mail_links()

input()
driver.close()
driver.quit()

for href in hrefs:
    driver.get(href)
    pass

input()

driver.close()
driver.quit()
