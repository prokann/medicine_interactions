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
from .models import *


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

            # extract data from page
            name = driver.find_element(By.CSS_SELECTOR, 'h1.drug-card__title.drug-card__title_map').text
            real_name = re.split('\d+', name)[0].replace("®", "")[:-1]
            # name = driver.find_element(By.CSS_SELECTOR, 'h1.drug-card__title.drug-card__title_map').text.split(',')[0]
            print(real_name)

            category = driver.find_elements(By.CSS_SELECTOR, 'a.breadcrumbs-site__list-link')[-1].text
            print(category)

            extracted_components = []
            # try except is not necessary
            try:
                composition = driver.find_elements(By.XPATH,
                                            '//h2[@id="anchor1"]/following::p[following::b[text()="Лікарська форма"]]')
                components = [i.text for i in composition]

                for component in components:
                    matches = re.findall(r'[.,;:]?\s*([\w\s\(\)\d%]+)[.,;:]?\s*', component)
                    formatted_components = [match.strip('.,;:') for match in matches]
                    extracted_components.extend(formatted_components)

                for component in extracted_components:
                    if 'містять' in component or 'містить' in component or 'допоміжні речовини' in component \
                            or 'допоміжна речовина' in component or 'діюча речовина' in component \
                            or 'діючі речовини' in component:
                        extracted_components.remove(component)

            except Exception as e:
                print(e)

            print(extracted_components)

            # Medicaments(name=real_name, category=category, composition=extracted_components).save()

            driver.close()
            # time.sleep(2)

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_selector)))

    except Exception as e:
        print(e)
        pass

    driver.quit()


def compare_medicines():
    pass


while button_more:
    try:
        button_more.click()
    except Exception as e:
        break
take_data()
