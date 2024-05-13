from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


def process_luke_sett(driver, luke_sett_rows):
    dismantling_checkbox = luke_sett_rows[0].find_element(By.ID, 'pegass_sett__dismantling')
    coup_checkbox = luke_sett_rows[0].find_element(By.ID, 'pegass_sett__coup')
    
    coup_checkbox.click()
    dismantling_checkbox.click()

def create_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    
    chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
    service = ChromeService(executable_path=chrome_driver_path)
    
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def b2b(imei):
    driver = create_chrome_driver()
    try:
        driver.get('https://911.fm/adm/?luke')

        imei_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="num"]'))
        )
        print('Found imei field')
        imei_input.send_keys(imei)
        imei_input.send_keys(Keys.ENTER)
        print('Entered imei')

        change_owner_element = driver.find_element(By.CSS_SELECTOR, 'span.owner')
        change_owner_element.click()

        phone_input = driver.find_element(By.CSS_SELECTOR, 'input#num')
        if phone_input.get_attribute('value'):
            phone_input.clear()

        phone_input.send_keys('+79531531372')
        submit_button = driver.find_element(By.ID, 'btnChange')
        submit_button.click()
        print('Clicked on change owner')

        luke_sett_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'luke_sett'))
        )

        process_luke_sett(driver, luke_sett_rows)

        button_element = driver.find_element(By.XPATH, '//tr[@class="luke_sett"]//button[@class="tgpssave"]')
        button_element.click()
        print('Clicked on save changes')

    finally:
        driver.quit()

def b2c(imei):
    driver = create_chrome_driver()

    try:
        driver.get('https://911.fm/adm/?luke')

        imei_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="num"]'))
        )
        imei_input.send_keys(imei)
        imei_input.send_keys(Keys.ENTER)

        luke_sett_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'luke_sett'))
        )

        process_luke_sett(driver, luke_sett_rows)

        button_element = driver.find_element(By.XPATH, '//tr[@class="luke_sett"]//button[@class="tgpssave"]')
        button_element.click()

    finally:
        driver.quit()

def change_1_min_GPS():
    driver = create_chrome_driver()

    try:
        driver.get('https://911.fm/adm/?luke')

        imei_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="num"]'))
        )
        imei_input.send_keys(imei)
        imei_input.send_keys(Keys.ENTER)

        luke_sett_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'luke_sett'))
        )

        parking_checkbox = luke_sett_rows[1].find_elements(By.TAG_NAME, 'td')[7].find_element(By.TAG_NAME, 'input')
        parking_checkbox.click()

        gps_min_input = luke_sett_rows[1].find_elements(By.TAG_NAME, 'td')[1].find_element(By.CLASS_NAME, 'dp_tgps')
        gps_min_input.clear()
        gps_min_input.send_keys("1")

        button_element = driver.find_element(By.XPATH, '//tr[@class="luke_sett"]//button[@class="tgpssave"]')
        button_element.click()

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        driver.quit()


