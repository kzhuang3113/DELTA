from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

SLEEP_TIME = 5
SHORT_SLEEP = 1
START_DATE = '04/07/2024'
END_DATE = '06/07/2024'
FLIGHT_LIST = ['flight-results-grid-0','flight-results-grid-1','flight-results-grid-2',
               'flight-results-grid-3','flight-results-grid-4','flight-results-grid-5',
               'flight-results-grid-6', 'flight-results-grid-7', 'flight-results-grid-8',
               'flight-results-grid-9', 'flight-results-grid-10', 'flight-results-grid-11',
               'flight-results-grid-12', 'flight-results-grid-13', 'flight-results-grid-14',
               ]
departure_dates = ["02/07/2024", "02/08/2024", "02/09/2024"]

def get_valid_date():
    while True:
        date_str = input("Please enter a date in the format (MM/DD/YYYY): ")
        try:
            # Attempt to parse the input date string
            date = datetime.strptime(date_str, "%m/%d/%Y")
            if date < date.now():
                raise ValueError
            return date_str  # Return the date string
        except ValueError:
            print("Invalid date format. Please try again.")

driver = webdriver.Chrome()
driver.get("https://www.delta.com/flight-search/book-a-flight")

# select one way

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
#input("Press Enter to continue")
# agree to privacy policy
understand_xpath = '/html/body/ngc-cookie-banner/div/div/div/div[2]/button'
understand_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, understand_xpath)))
understand_element.click()
time.sleep(SHORT_SLEEP)
#get the departure date input from the console
departure_date = get_valid_date()
departure_date_reformat = datetime.strptime(departure_date,"%m/%d/%Y")
current_date = datetime.now()
if departure_date_reformat < current_date:
    print('the departure date should not be in the past')

month_gap = departure_date_reformat.month - current_date.month

# activate the departure date selection window
departure_date_xpath = '//*[@id="input_departureDate_1"]'
departure_date_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, departure_date_xpath)))
departure_date_element.click()
time.sleep(SHORT_SLEEP)

# if the departure date is not in current month or next month, then need to click the next button till the month is located
while month_gap >1:
    month_gap -=1
    next_month_xpath = '//*[@id="booking"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[1]/a[2]/span'
    next_month_element =  WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH,next_month_xpath)))
    next_month_element.click()

departure_date_select_xpath = '//a[contains(@data-date,"{}")]'.format(departure_date)
departure_date_select_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, departure_date_select_xpath)))
time.sleep(SLEEP_TIME)
departure_date_select_element.click()
date_done_xpath = '//*[@id="booking"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[' \
                  '4]/div/div[3]/button[2]'
date_done_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, date_done_xpath)))
# driver.execute_script("arguments[0].scrollIntoView(true);", date_done_element)

date_done_element.click()

# choose cabin
# cabin_select_xpath = '//*[@id="booking"]/form/div[2]/div/div[1]/div[2]/span/span[1]'
# cabin_select_element = WebDriverWait(driver, SLEEP_TIME). \
#     until(EC.presence_of_element_located((By.XPATH, cabin_select_xpath)))
# cabin_select_element.click()
# premium_select_xpath = '//*[@id="ui-list-faresFor4"]'
# premium_select_element = WebDriverWait(driver, SLEEP_TIME). \
#     until(EC.presence_of_element_located((By.XPATH, premium_select_xpath)))
# time.sleep(SLEEP_TIME)
# premium_select_element.click()
# time.sleep(SLEEP_TIME)

# search for flight details
search_xpath = '//*[@id="btnSubmit"]'
search_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, search_xpath)))
search_element.click()
time.sleep(10)

# get all the price and cabin info by iterate through the flight id one by one
input("Press Enter to continue")
with open('flight.txt','w',encoding='utf-8') as f:
    for flight_id in FLIGHT_LIST:
        div_element = driver.find_element(By.ID, flight_id)
        price_xpath = ".//span[@class='fare-cell-rounded-amount ng-star-inserted']"
        price_elements = div_element.find_elements(By.XPATH, value=price_xpath)
        flight_numbers_xpath = ".//span[@_ngcontent-shopping-slice-c239]"
        flight_numbers_elements = div_element.find_elements(By.XPATH,value=flight_numbers_xpath)
        # flight_number_xpath = ".//idp-flight-card/div/div/idp-flight-card-info/div/div[1]/a/span"
        # flight_numbrt = div_element.find_element(by=By.XPATH,value=flight_number_xpath)
        flight_duration_xpath = ".//idp-flight-card/div/div/idp-flight-card-info/div/div[2]"
        flight_duration = div_element.find_element(By.XPATH, value=flight_duration_xpath)
        for flight_number in flight_numbers_elements:
            print(f"flight number: {flight_number.text}",file=f)
        print(f'flight duration: {flight_duration.text}',file=f)
        # flight_non_stop_xpath = './/idp-flight-card/div/div/div[2]/idp-flight-card-path/div/div[2]'
        try:
            flight_non_stop = div_element.find_element(By.CLASS_NAME, value="flight-card-path__non-stop")
            print(flight_non_stop.text,file=f)
        except NoSuchElementException:
            try:
                flight_layovers = div_element.find_elements(By.CLASS_NAME, value="flight-card-path__layover-text")
                for _ in flight_layovers:
                    print(_.text,file=f)
            except NoSuchElementException:
                print('non stop and lay over not found',file=f)

        try:
            cabin_class = div_element.find_elements(By.CLASS_NAME, value="cell-brand-name")

        except NoSuchElementException:
            print('cabin info not found',file=f)

        price_list = [pe.text for pe in price_elements]
        cabin_list = [cabin.text for cabin in cabin_class]
        print(price_list[1:],file=f)
        print(cabin_list,file=f)




input("Press Enter to close the window")
driver.quit()

