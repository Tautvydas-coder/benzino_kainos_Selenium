from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FoxService

CHROME_DRIVER_PATH = "C:/Users/takvietk/Downloads/Programos/chromedriver_win32_103/chromedriver"
FFOX_DRIVER_PATH = "C:/Users/takvietk/Downloads/Programos/geckodriver-v0.31.0-win64/geckodriver"


def driver_service():
    # ser = Service(CHROME_DRIVER_PATH)
    ser = FoxService(FFOX_DRIVER_PATH)
    # driver = webdriver.Chrome(service=ser)
    driver = webdriver.Firefox(service=ser)
    return driver
