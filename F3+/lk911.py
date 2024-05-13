from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service as ChromeService


# Function to perform the common login steps
def perform_login(driver, phone, password):
    driver.get('https://lk.911.fm/')
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="f_myion_ul"]')))
    phone_input.send_keys(phone)
    print("Phone number entered")
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="f_myion_uh"]')))
    password_input.send_keys(password)
    print("Password entered")
    password_input.send_keys(Keys.ENTER)
    print("Clicked on the Login button")


def change_settings(driver, value, ccid, switch_element=None):
    label_objects = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//label[text()="Объекты"]')))
    label_objects.click()
    print("Clicked on 'Объекты' label")

    span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'span[title="{ccid}"]')))
    span.click()
    print("Clicked on the element")

    time.sleep(1)  # Introduce a delay

    pegass_item_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//div[@class="pegass_item_content"][contains(text(), "Изменить режим")]')))
    pegass_item_content.click()
    print("Clicked on 'Изменить режим'")

    time.sleep(1)  # Introduce a delay

    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="pegass_itemRadio" and label="Поиск"]/span')))
    search_button.click()
    print("Clicked on 'Поиск'")

    time.sleep(1)  # Introduce a delay

    select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[device_user_settings="131"]'))))
    select.select_by_value(str(value))
    print(f"Changed the value of the <select> to '{value}'")

    if switch_element:
        time.sleep(1)  # Introduce a delay
        switch_element.click()
        print(f"Clicked on {switch_element.get_attribute('id')}")


# Function to change the 5-minute setting
def change_5min(imei):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    service = ChromeService(executable_path=chrome_driver_path)

    with webdriver.Chrome(service=service, options=options) as driver:
        try:
            perform_login(driver, '+79531531372', 'jcVoZpxw0')
            change_settings(driver, 5, imei)
            save_icon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mi-check')))
            save_icon.click()
            print("Clicked on the element")

        except Exception as e:
            print(f'An error occurred: {e}')
        print("Web browser closed")


# Function to change the ACC setting
def change_ACC(ccid, chrome_driver_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    service = ChromeService(executable_path=chrome_driver_path)

    with webdriver.Chrome(service=service, options=options) as driver:
        try:
            perform_login(driver, '+79531531372', 'jcVoZpxw0')
            change_settings(driver, 5, ccid)

            # Wait for the span element inside the div to be clickable
            switch_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@class="pegass_itemSwitch" and @device_user_settings="19"]')
                )
            )
            driver.execute_script('arguments[0].setAttribute("value", "1")', switch_element)
            print("Changed value to '1'")
            save_icon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mi-check')))
            save_icon.click()
            print("Clicked on the ACC element")
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            print("Web browser closed")


chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
