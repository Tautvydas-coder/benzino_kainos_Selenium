from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import mail_credentials
from webdriver_service import driver_service
from selenium.webdriver.support.select import Select

driver = driver_service()
driver.get('chrome://settings/clearBrowserData')
City = 'Vilnius'

def open_website():
    driver.implicitly_wait(5)
    driver.get("http://www.degalukainos.lt/")


def choose_city():
    select_element = driver.find_element(By.ID, 'city')
    select_object = Select(select_element)
    select_object.select_by_visible_text(City)


def press_button():
    driver.find_element(By.XPATH, "//input[@value='Ieškoti']").click()


def fetch_address_and_price():
    main = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="kainos"]/tbody'))
    )
    rows_table = main.find_elements(By.TAG_NAME, "tr")
    list_of_address_prices = []
    for row_table in rows_table:
        columns = row_table.find_elements(By.TAG_NAME, "td")
        list_of_address_prices.append((columns[2].text, columns[4].text))
    list_of_address_prices.sort(key=lambda i: i[1])
    address_and_price_tuple = list(filter(lambda x: x[1] != ("-" or "A95"), list_of_address_prices))[0]
    address_and_price_string = ' '.join(address_and_price_tuple)
    return address_and_price_string


def open_new_tab():
    driver.switch_to.new_window('tab')


def goto_gmail_web():
    driver.get(
        'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service'
        '=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')


def input_login_name(login_name: str):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
    ).send_keys(login_name)
    driver.find_element(By.XPATH, "//div[@id='identifierNext']/div/button/span").click()


def input_login_password(login_password: str):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
    ).send_keys(login_password)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]').click()


def create_letter():
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div'))
    ).click()


def input_sender_email(sender_mail: str):
    driver.implicitly_wait(15)
    sender_address = driver.find_element(By.XPATH,
                                         '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div['
                                         '3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td['
                                         '2]/div/div/textarea')
    ActionChains(driver).click(sender_address).send_keys(sender_mail + Keys.ENTER).perform()


def input_letter(address_and_price: str):
    mail_content = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,
                                        '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div['
                                        '3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[1]/div['
                                        '2]/div[1]/div/table/tbody/tr/td[2]'))
    )
    ActionChains(driver).move_to_element(mail_content).click(mail_content).send_keys(address_and_price).perform()


def send_email():
    button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,
                                        '/html/body/div[20]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div['
                                        '3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div['
                                        '4]/table/tbody/tr/td[1]/div/div[2]'))
    )
    ActionChains(driver).move_to_element(button).click().perform()


if __name__ == '__main__':
    open_website()
    choose_city()
    press_button()
    address_price = fetch_address_and_price()
    open_new_tab()
    goto_gmail_web()
    email_name = mail_credentials.email_name()
    email_password = mail_credentials.email_password()
    input_login_name(email_name)
    input_login_password(email_password)
    create_letter()
    input_sender_email(email_name)
    input_letter(address_price)
    send_email()
    # driver.close()
