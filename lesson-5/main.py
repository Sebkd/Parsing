from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from secret import LOGIN, PASSWORD

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# driver = webdriver.Chrome(executable_path='./chromedriver')

driver.get('https://gb.ru/login')

element = driver.find_element(By.ID, 'user_email')
element.send_keys(LOGIN)

element = driver.find_element(By.ID, 'user_password')
element.send_keys(PASSWORD)

element.send_keys(Keys.ENTER) # имитация нажатия клавиши

input('continue')
# print()
#
#
# while True:
#
#
#     pass
#
driver.close()
