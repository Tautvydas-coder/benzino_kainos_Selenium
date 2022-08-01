from selenium import webdriver
from selenium.webdriver.chrome.service import Service

CHROME_DRIVER_PATH = "C:/Users/takvietk/Downloads/Programos/chromedriver_win32_103/chromedriver"


def driver_service():
    ser = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=ser)
    return driver
