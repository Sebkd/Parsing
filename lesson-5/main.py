from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from secret import LOGIN, PASSWORD

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# driver = webdriver.Chrome(executable_path='./chromedriver')

driver.get('https://gb.ru/login')

element = driver.find_element(By.ID, 'user_email')
element.send_keys(LOGIN)

element = driver.find_element(By.ID, 'user_password')
element.send_keys(PASSWORD)

element.send_keys(Keys.ENTER)  # имитация нажатия клавиши

element = driver.find_element(By.XPATH, '//a[contains(@href, "/users/")]')
href = element.get_attribute('href')
driver.get(href)  # переход по ссылке selenium нам построить абсолютный путь, второй раз потому что есть косяк на сайте

element = driver.find_element(By.XPATH, '//a[contains(@href, "/users/")]')
href = element.get_attribute('href')
driver.get(href)  # переход по ссылке selenium нам построить абсолютный путь

element = driver.find_element(By.CLASS_NAME, 'text-sm')
href = element.get_attribute('href')
driver.get(href)  # переход по ссылке selenium нам построить абсолютный путь

hours = driver.find_element(By.NAME, 'user[time_zone]')
select = Select(hours)
select.select_by_value('Moscow')

hours.submit()  # сохранить состояние формы

print()

driver.close()
