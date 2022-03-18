'''
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: stu*****@mail.ru
Пароль тестового ящика: *********
'''


from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

from secret import LOGIN_MAIL, PASSWORD_MAIL

service = Service('./chromedriver')

chrome_options = Options()  # для работы с опциями браузера, например чтобы он открылся на полный экран
chrome_options.add_argument('start-maximized')  # полный экран
ua='cat'
chrome_options.add_argument('--user-agent=%s' % ua)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

driver.get('https://mail.ru/')

element = driver.find_element(By.ID, 'mailbox__login')
element.send_keys(LOGIN_MAIL)

element = driver.find_element(By.ID, 'mailbox__password')
element.send_keys(PASSWORD_MAIL)

element.send_keys(Keys.ENTER)  # имитация нажатия клавиши
