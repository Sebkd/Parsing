from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

service = Service('./chromedriver')

chrome_options = Options()  # для работы с опциями браузера, например чтобы он открылся на полный экран
chrome_options.add_argument('start-maximized')  # полный экран
ua='cat'
chrome_options.add_argument('--user-agent=%s' % ua)

driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.implicitly_wait(10)

driver.get('https://pikabu.ru/')

for i in range(5):
    articles = driver.find_elements(By.TAG_NAME, 'article')
    actions = ActionChains(driver) #накапливает события как стек
    actions.move_to_element(articles[-1])
    actions.perform()
    time.sleep(4)
