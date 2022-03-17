from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# service = Service(ChromeDriverManager().install())
service = Service('./chromedriver')

chrome_options = Options()  # для работы с опциями браузера, например чтобы он открылся на полный экран
chrome_options.add_argument('start-maximized')  # полный экран

driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.implicitly_wait(10) # ждем 10 секунд до появления события, без использования WebDriverWait и expected_conditions

driver.get('https://5ka.ru/special_offers')

# button = driver.find_element(By.XPATH, '//span[contains(text(), "Принять")]')
# button.click()

# выбор местоположения
button = driver.find_element(By.XPATH, "//span[contains(text(), 'Да, верно')]")
button.click()

# принимаем печенку
button = driver.find_element(By.XPATH, '//p[contains(text(), "cookie")]/..//span[contains(text(), "Принять")]')
button.click()

# принимаем технические работы - не всегда бывает
button = driver.find_element(By.XPATH, '//b[contains(text(), "Технические")]/../..//span[contains(text(), "Принять")]')
button.click()

index = 0
while index < 20:
    wait = WebDriverWait(driver, 10)  # тоже самое что driver.implicitly_wait(10)
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'add-more-btn')))

    # button = driver.find_element(By.CLASS_NAME, 'add-more-btn')
    button.click()  # кликаем по элементу
    index += 1

print()

driver.close()
