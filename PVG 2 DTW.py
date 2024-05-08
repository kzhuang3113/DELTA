import sys
import os

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
SHORT_SLEEP = 3

FLIGHT_LIST = ['flight-results-grid-0', 'flight-results-grid-1', 'flight-results-grid-2',

               ]


# PREMIUM_SELECT_GRID = ["grid-row-0-fare-cell-desktop-DPPS", "grid-row-1-fare-cell-desktop-DPPS"
#                        ]


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


def calendar_popup():
    calendar_xpath = '//*[@id="calDepartLabelCont"]/span[2]'
    calendar_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, calendar_xpath)))
    calendar_element.click()
    time.sleep(SHORT_SLEEP)


def date_selection(date, is_return):
    date_reformat = datetime.strptime(date, "%m/%d/%Y")
    if date_reformat < datetime.now():
        print('the departure/return date should not be in the past')
    if not is_return:
        gap = date_reformat.month - datetime.now().month
    else:
        gap = date_reformat.month - departure_date_reformat.month
    calendar_popup()
    while gap > 1:
        gap -= 1
        next_month_path = ('//*[@id="booking"]/form/div[1]/div/div[1]/div[1]/div['
                           '3]/date-selection-view/div/div/div/div/div[4]/div/div[1]/a[2]/span')
        next_month_navigator = WebDriverWait(driver, SLEEP_TIME). \
            until(EC.presence_of_element_located((By.XPATH, next_month_path)))
        next_month_navigator.click()

    date_select_xpath = '//a[contains(@data-date,"{}")]'.format(date)
    date_select_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, date_select_xpath)))
    time.sleep(SLEEP_TIME)
    date_select_element.click()
    date_set_xpath = '//*[@id="booking"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[' \
                     '4]/div/div[3]/button[2]'
    date_set_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, date_set_xpath)))

    date_set_element.click()


def get_departure_flight_detail(web_driver, departure_css):
    flight_card = driver.find_element(By.CSS_SELECTOR, departure_css)
    outbound_flight_numbers = flight_card.find_elements(By.CLASS_NAME, 'flight-number')
    for outbound_flight_number in outbound_flight_numbers:
        print(f'out bound flight number: {outbound_flight_number.text}')
    outbound_flight_duration = flight_card.find_element(By.CLASS_NAME, 'flight-duration')
    print(f'out bound flight duration: {outbound_flight_duration.text}')
    schedule_times = flight_card.find_elements(By.CLASS_NAME, 'schedule-time')
    print(f'departure time: {schedule_times[0].text}')
    print(f'arrival time: {schedule_times[1].text}')
    transition_detail = 'transition: '
    try:
        direct_flight = flight_card.find_element(By.CLASS_NAME, value="flight-card-path__non-stop")
        transition_detail = transition_detail + direct_flight.text
        print(transition_detail)
    except NoSuchElementException:
        try:
            transition_flight = flight_card.find_elements(By.CLASS_NAME, value="flight-card-path__layover-text")
            for _ in transition_flight:
                transition_detail += _.text
            print(transition_detail)
        except NoSuchElementException:
            print('non stop and lay over not found')


def get_return_flight_details():
    for flight in FLIGHT_LIST:
        flight_info_element = driver.find_element(By.ID, flight)
        flight_numbers = flight_info_element.find_elements(By.CLASS_NAME, 'flight-number')

        # input('continue after checking the price and cabin elements')
        flight_numbers = flight_info_element.find_elements(By.CLASS_NAME, 'flight-number')
        flight_time_xpath = ".//idp-flight-card/div/div/idp-flight-card-info/div/div[2]"
        flight_time = flight_info_element.find_element(By.XPATH, value=flight_time_xpath)
        for _ in flight_numbers:
            print(f"flight number: {_.text}")
        print(f'flight duration: {flight_time.text}')
        transition_detail = 'transition: '
        try:
            flight_no_stop = flight_info_element.find_element(By.CLASS_NAME, value="flight-card-path__non-stop")
            transition_detail += flight_no_stop.text
            print(transition_detail)
        except NoSuchElementException:
            try:
                flight_stop_by = flight_info_element.find_elements(By.CLASS_NAME,
                                                                   value="flight-card-path__layover-text")
                for _ in flight_stop_by:
                    transition_detail += _.text
                print(transition_detail)
            except NoSuchElementException:
                print('non stop and lay over not found')

        price_and_cabin_elements = flight_info_element.find_elements(By.XPATH, ".//*[contains(@class, 'fare-cell-item "
                                                                               "ng-star-inserted')]")
        for item in price_and_cabin_elements:
            cabin = item.find_elements(By.CLASS_NAME, 'cell-brand-name')
            cabin_info = 'cabin info: '
            for _ in cabin:
                cabin_info = cabin_info + _.text
            print(cabin_info)
            price = item.find_elements(By.XPATH, ".//*[contains(@class, 'fare-cell-rounded-amount ng-star-inserted')]")
            price_info = 'price info: '
            for _ in price:
                price_info = price_info + _.text
            print(price_info)
        print('***************************************************************')
    print('This is a new search ##################')


def select_premium_economy(flight_info_id):
    wait = WebDriverWait(driver, 10)
    flight_info_div = wait.until(EC.presence_of_element_located((By.ID, flight_info_id)))
    try:
        premium_select_div = flight_info_div.find_element(By.XPATH, ".//div[@class='cell-brand-name' and contains(text(), "
                                                                "'Premium Select')]")
        time.sleep(10)
        premium_select_div.click()
        time.sleep(30)
    except NoSuchElementException:
        print('no premium economy offering found')
        return

    select_flight_button = driver.find_element(By.CLASS_NAME, "flight-specific_amenities__details-button")
    select_flight_button.click()
    continue_button_xpath = ('/html/body/idp-root/div/div[2]/idp-search-results/div/idp-refundable-modal/div/idp-simple'
                             '-modal/div/div[1]/div/div[2]/idp-refundable-upsell-modal/div/div/div['
                             '1]/idp-refundable-brand-details/div/div/idp-refundable-brand-details-footer/div/idp'
                             '-button'
                             '/button')
    continue_button_element = WebDriverWait(driver, SLEEP_TIME). \
        until(EC.presence_of_element_located((By.XPATH, continue_button_xpath)))
    continue_button_element.click()


driver = webdriver.Chrome()
driver.get("https://www.delta.com/flight-search/book-a-flight")

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
time.sleep(SHORT_SLEEP)
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
time.sleep(SHORT_SLEEP)
to_input_element.send_keys(Keys.RETURN)

# agree to privacy policy
understand_xpath = '/html/body/ngc-cookie-banner/div/div/div/div[2]/button'
understand_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, understand_xpath)))
understand_element.click()
time.sleep(SHORT_SLEEP)

# get the departure/return date input from the console and set the dates

return_flag = False
departure_date = get_valid_date()
date_selection(departure_date, return_flag)
return_date = get_valid_date()
departure_date_reformat = datetime.strptime(departure_date, "%m/%d/%Y")
return_date_reformat = datetime.strptime(return_date, "%m/%d/%Y")
if return_date_reformat < departure_date_reformat:
    print('return date need to be later than departure date')
return_flag = True
date_selection(return_date, return_flag)

# search for flight details
search_xpath = '//*[@id="btnSubmit"]'
search_element = WebDriverWait(driver, SLEEP_TIME). \
    until(EC.presence_of_element_located((By.XPATH, search_xpath)))
search_element.click()
time.sleep(30)

# get all the price and cabin info by iterate through the flight id one by one

current_url = driver.current_url
output_file = 'flight_details.txt'
if os.path.exists(output_file):
    os.remove(output_file)
original_stdout = sys.stdout
for air_flight in FLIGHT_LIST:
    with open(output_file, 'a', encoding='utf-8') as f:
        sys.stdout = f
        print(f'departure date: {departure_date}')
        get_departure_flight_detail(driver, f'#{air_flight} .flight-results-grid__flight-card')
    select_premium_economy(air_flight)
    time.sleep(10)
    with open(output_file, 'a', encoding='utf-8') as f:
        sys.stdout = f
        print(f'return date:  {return_date}')
        # sys.stdout = original_stdout
        get_return_flight_details()

    driver.execute_script("window.open('{}', '_blank');".format(current_url))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(30)
sys.stdout = original_stdout
input('iteration done, press enter to quit')
driver.quit()
