import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import os
from threading import Thread
import keyboard

#global var
stop = 0

#options for driver
opts = Options()
opts.add_argument("--disable-blink-features=AutomationControlled")

#xpath
xpath_place_from = '//*[@id="application"]/div[1]/div[2]/div[1]/div[5]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[2]'
xpath_place_from_interactable = '//*[@id="application"]/div[1]/div[2]/div[1]/div[5]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/span[1]/span[2]/textarea'
xpath_place_where_interactable = '//*[@id="application"]/div[1]/div[2]/div[1]/div[5]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/span[1]/span[2]/textarea'
x_path_cost = '//*[@id="application"]/div[1]/div[2]/div[1]/div[5]/div/div[1]/div/div[2]/div/div/div/button[1]/span[2]/span[3]/span[2]'
x_path_cost_another = '//*[@id="application"]/div[1]/div[2]/div[1]/div[5]/div/div[1]/div/div[2]/div/div/div/button[1]/span[2]/span[3]/span[3]'

#URL
URL = "https://taxi.yandex.ru/ru_ru/"

#path to cookie
cookie_name = "\cook.json"
path_cook = os.path.abspath(os.curdir) + cookie_name

def exit_check():
    global stop
    while True:
        if keyboard.is_pressed("p"):
            stop = 1
            break
def save_cookie(driver, path):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        driver.add_cookie(cookie)

def check_auto():
    if os.path.exists(path_cook):
        print("Файл авторизации уже существует")
        return True
    else:
        driver = webdriver.Chrome(service=service)
        driver.get(URL)
        print("Необходимо авторизоваться")
        input("После авторизации введите любую букву/цифру в консоль\n")
        save_cookie(driver, path_cook)
        print("Перезапустите программу")
        time.sleep(20)
        return False


def write_adress(adress):
    time.sleep(3)
    adress.find_element(By.XPATH, xpath_place_from).click()
    time.sleep(1)
    adress.find_element(By.XPATH, xpath_place_from_interactable).send_keys(Keys.CONTROL + "a")
    adress.find_element(By.XPATH, xpath_place_from_interactable).send_keys(Keys.DELETE)
    time.sleep(1)
    adress.find_element(By.XPATH, xpath_place_from_interactable).send_keys(place_from)
    time.sleep(2)
    adress.find_element(By.XPATH, xpath_place_from_interactable).send_keys(Keys.DOWN)
    time.sleep(2)
    adress.find_element(By.XPATH, xpath_place_from_interactable).send_keys(Keys.ENTER)
    time.sleep(2)
    adress.find_element(By.XPATH, xpath_place_where_interactable).send_keys(place_where)
    time.sleep(2)
    adress.find_element(By.XPATH, xpath_place_where_interactable).send_keys(Keys.DOWN)
    time.sleep(2)
    adress.find_element(By.XPATH, xpath_place_where_interactable).send_keys(Keys.ENTER)
    time.sleep(2)
    adress.execute_script("window.open()")
    time.sleep(2)
    adress.switch_to.window(adress.window_handles[1])
    adress.switch_to.window(adress.window_handles[0])
    time.sleep(2)

def calculate_cost(driver):
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        cost = driver.find_element(By.XPATH, x_path_cost)
        if cost.text.strip() == '':
            cost = driver.find_element(By.XPATH, x_path_cost_another)
        return cost.text

if __name__ == "__main__":
    if check_auto():
        service = Service(ChromeDriverManager().install())
        with open('place.txt', 'r', encoding="utf-8") as data:
            place_from = data.readline().strip()
            place_where = data.readline().strip()
        driver = webdriver.Chrome(service=service, options=opts)
        driver_2 = webdriver.Chrome(service=service, options=opts)
        driver_2.set_window_position(950, 10)
        driver.get(URL)
        driver_2.get(URL)
        load_cookie(driver, path_cook)
        load_cookie(driver_2, path_cook)
        driver.get(URL)
        driver_2.get(URL)
        write_adress(driver)
        write_adress(driver_2)
        cost_driver_1 = int(calculate_cost(driver)[:-1].strip())
        cost_driver_2 = int(calculate_cost(driver_2)[:-1].strip())
        min_cost = min(cost_driver_1, cost_driver_2)
        thread1 = Thread(target=exit_check)
        thread1.start()
        while True:
            if stop == 1:
                input('Программа приостановлена')
            else:
                if cost_driver_2 > cost_driver_1:
                    cost_driver_2 = int(calculate_cost(driver_2)[:-1].strip())
                    print(f'Обновил 2 браузер, цена: {cost_driver_2}, начальная минимальная цена: {min_cost}')
                else:
                    cost_driver_1 = int(calculate_cost(driver)[:-1].strip())
                    print(f'Обновил 1 браузер, цена: {cost_driver_1}, начальная минимальная цена: {min_cost}')



