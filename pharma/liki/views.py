from django.shortcuts import render
# import requests
import time, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


s = Service('C:\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://apteki.ua/uk/kategoriya-ufc/001f00000000')
wait = WebDriverWait(driver, 10)

xpath_selector = '//a[.//span[@class="block font-bold truncate-3"]]'
button_more = driver.find_element(By.CSS_SELECTOR, 'button.btn-more')
elements = []


def take_data():
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_selector)))

        for i in range(len(elements)):
            ActionChains(driver).key_down(Keys.CONTROL).click(elements[i]).key_up(Keys.CONTROL).perform()

            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            #do
            name = driver.find_element(By.CSS_SELECTOR, 'h1.drug-card__title.drug-card__title_map').text
            real_name = re.split('\d+', name)[0].replace("®", "")[:-1]
            # name = driver.find_element(By.CSS_SELECTOR, 'h1.drug-card__title.drug-card__title_map').text.split(',')[0]
            print(real_name)

            category = driver.find_elements(By.CSS_SELECTOR, 'a.breadcrumbs-site__list-link')[-1]
            composition = driver.find_elements(By.XPATH,
                                '//i[text()="діюча речовина: "]/following::p[following::b[text()="Лікарська форма"]]')
            if not composition:
                composition = driver.find_elements(By.XPATH,
                                '//i[text()="діюча речовина:"]/following::p[following::b[text()="Лікарська форма"]]')
            # composition = [i.text for i in composition]
            # components = [i.text.split() for i in composition]
            components = [item for sublist in [i.text.split() for i in composition] for item in sublist]

            driver.close()
            time.sleep(2)

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)

            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_selector)))

    except Exception as e:
        print(e)
        pass

    driver.quit()


# while button_more:
#     try:
#         button_more.click()
#     except Exception as e:
#         break
take_data()
