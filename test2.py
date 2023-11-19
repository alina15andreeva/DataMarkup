from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from pymongo import MongoClient


options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)
driver.get("https://www.ozon.ru/")

time.sleep(20)

input_field = driver.find_element(By.NAME, "text")
input_field.send_keys("VR очки Shinecon")
input_field.send_keys(Keys.ENTER)

client = MongoClient(host='localhost', port=27017)
db = client['ozon_products']
collection = db['vr_glasses']

while True:
    while True:
        wait = WebDriverWait(driver, 50)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x7i']")))

        print(len(cards))
        count = len(cards)
        driver.execute_script("window.scrollBy(0,2000)")
        time.sleep(3)
        cards = driver.find_elements(By.XPATH, "//div[@class='x7i']")
        if len(cards) == count:
            break

    for card in cards:
        try:
            price = card.find_element(By.XPATH, ".//div[contains(@class, 'c3118-a0')]").text
            name = card.find_element(By.XPATH, ".//div[contains(@class, 'b7a')]//span[contains(@class, 'tsBody500Medium')]").text
            url = card.find_element(By.XPATH, ".//a[contains(@class, 'tile-hover-target')]").get_attribute("href")

            product_data = {
                "name": name,
                "price": price,
                "url": url
            }

            collection.insert_one(product_data)
            #print(name, price, url)
        except Exception as e:
            print("Error:", e)

    try:
        button = driver.find_element(By.CLASS_NAME, "a2429-e7")
        actions = ActionChains(driver)
        actions.move_to_element(button).click()  
        actions.perform()
    except:
        break
