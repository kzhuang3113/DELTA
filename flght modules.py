from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
import time

SLEEP_TIME = 2
SHORT_SLEEP = 0.5
START_DATE = '02/07/2024'
END_DATE = '04/07/2024'
FLIGHT_LIST = ['flight-results-grid-0', 'flight-results-grid-1', 'flight-results-grid-2',
               'flight-results-grid-3', 'flight-results-grid-4', 'flight-results-grid-5',
               'flight-results-grid-6', 'flight-results-grid-7', 'flight-results-grid-8',
               'flight-results-grid-9', 'flight-results-grid-10', 'flight-results-grid-11',
               'flight-results-grid-12', 'flight-results-grid-13', 'flight-results-grid-14',
               ]

driver = webdriver.Chrome()


def open_url(web_url):
    driver.get(web_url)


# select one way
def select_oneway():
    trip_select_xpath = '//*[@id="booking"]/form/div[1]/div/div[1]/div[1]/div[2]/span/span[1]'
    trip_select_element = origin_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, trip_select_xpath))
              )
    trip_select_element.click()
    time.sleep(SHORT_SLEEP)
    oneway_xpath = '//*[@id="ui-list-selectTripType1"]'
    oneway_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, oneway_xpath))
              )
    oneway_element.click()
    time.sleep(SLEEP_TIME)


# select original city and target city
def select_cities():
    origin_xpath = '//*[@id="fromAirportName"]'
    origin_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, origin_xpath))
              )
    origin_element.click()
    time.sleep(SLEEP_TIME)
    origin_input_xpath = '//*[@id="search_input"]'
    origin_input_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, origin_input_xpath))
              )
    time.sleep(SLEEP_TIME)
    origin_input_element.send_keys('DTW')
    time.sleep(SLEEP_TIME)
    origin_input_element.send_keys(Keys.RETURN)

    to_xpath = '//*[@id="toAirportName"]'
    to_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, to_xpath))
              )
    to_element.click()
    time.sleep(SLEEP_TIME)
    to_input_xpath = '//*[@id="search_input"]'
    to_input_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, to_input_xpath)))
    time.sleep(SLEEP_TIME)
    to_input_element.send_keys('PVG')
    time.sleep(SLEEP_TIME)
    to_input_element.send_keys(Keys.RETURN)


# agree to privacy policy
def accept_tnc():
    understand_xpath = '/html/body/ngc-cookie-banner/div/div/div/div[2]/button'
    understand_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, understand_xpath)))
    understand_element.click()
    time.sleep(SHORT_SLEEP)


# Select departure date
def set_departure_date(departure_date):
    # departure_date = "02/19/2024"
    departure_date_xpath = '//*[@id="input_departureDate_1"]'
    departure_date_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, departure_date_xpath)))
    departure_date_element.click()
    time.sleep(SHORT_SLEEP)
    departure_date_select_xpath = '//a[contains(@data-date,"{}")]'.format(departure_date)
    departure_date_select_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, departure_date_select_xpath)))
    time.sleep(SLEEP_TIME)
    departure_date_select_element.click()
    date_done_xpath = '//*[@id="booking"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[' \
                      '4]/div/div[3]/button[2]'
    date_done_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, date_done_xpath)))
    date_done_element.click()


# driver.execute_script("arguments[0].scrollIntoView(true);", date_done_element)


# choose cabin
def select_cabin():
    cabin_select_xpath = '//*[@id="booking"]/form/div[2]/div/div[1]/div[2]/span/span[1]'
    cabin_select_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, cabin_select_xpath)))
    cabin_select_element.click()
    premium_select_xpath = '//*[@id="ui-list-faresFor4"]'
    premium_select_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, premium_select_xpath)))
    time.sleep(SLEEP_TIME)
    premium_select_element.click()
    time.sleep(SLEEP_TIME)


# search for flight details
def search_flights():
    search_xpath = '//*[@id="btnSubmit"]'
    search_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    search_element.click()
    time.sleep(10)


# get all the price and cabin info by iterate through the flight id one by one
input("Press Enter to continue")


def get_flight_details():
    for flight_id in FLIGHT_LIST:
        div_element = driver.find_element(By.ID, flight_id)
        price_xpath = ".//span[@class='fare-cell-rounded-amount ng-star-inserted']"
        price_elements = div_element.find_elements(By.XPATH, value=price_xpath)
        flight_number_xpath = ".//idp-flight-card/div/div/idp-flight-card-info/div/div[1]/a/span"
        flight_numbrt = div_element.find_element(by=By.XPATH, value=flight_number_xpath)
        flight_duration_xpath = ".//idp-flight-card/div/div/idp-flight-card-info/div/div[2]"
        flight_duration = div_element.find_element(By.XPATH, value=flight_duration_xpath)
        print(f"flight number: {flight_numbrt.text}")
        print(f'flight duration: {flight_duration.text}')
        # flight_non_stop_xpath = './/idp-flight-card/div/div/div[2]/idp-flight-card-path/div/div[2]'
        try:
            flight_non_stop = div_element.find_element(By.CLASS_NAME, value="flight-card-path__non-stop")
            print(flight_non_stop.text)
        except:
            try:
                flight_layovers = div_element.find_elements(By.CLASS_NAME, value="flight-card-path__layover-text")
                for _ in flight_layovers:
                    print(_.text)
            except:
                print('non stop and lay over not found')

        try:
            cabin_class = div_element.find_elements(By.CLASS_NAME, value="cell-brand-name")

        except:
            print('cabin info not found')

        price_list = [pe.text for pe in price_elements]
        cabin_list = [cabin.text for cabin in cabin_class]
        print(price_list, cabin_list)


input("Press Enter to close the window")
driver.quit()
