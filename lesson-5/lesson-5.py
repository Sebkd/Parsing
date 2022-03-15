from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from secret import LOGIN, PASSWORD

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get('https://gb.ru/login')
element = driver.find_element(By.ID, 'user_email')
element.send_keys(LOGIN)
element.send_keys(PASSWORD)
while True:
    pass
