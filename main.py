from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
import time
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


options = webdriver.ChromeOptions()
# options.add_argument('--start_maximized')
options.add_argument("--headless")

# Initialize the web browser
driver = webdriver.Chrome(options=options)


while True:
    current_time = datetime.now().time()

    if current_time.hour == 14 and current_time.minute == 5 and current_time.second == 0:
        login_url = 'https://login.ufl.edu'
        driver.get(login_url)
        login_wait = WebDriverWait(driver, 5)

        username_input = driver.find_element(By.ID, 'username')
        username = config.get('username')
        username_input.send_keys(username)

        password_input = driver.find_element(By.ID, 'password')
        password = config.get('password')
        password_input.send_keys(password)

        submit_button = driver.find_element(By.ID, 'submit')
        submit_button.click()

        iframe = driver.find_element(By.ID, 'duo_iframe')
        driver.switch_to.frame(iframe)

        remember_button = driver.find_element(By.NAME, 'dampen_choice')
        remember_button.click()

        duo_push = driver.find_element(By.CLASS_NAME, 'auth-button')
        duo_push.click()

    if current_time.hour == 0 and current_time.minute == 0 and current_time.second == 0:
        # Define the desired date and times
        current_date = datetime.now()

        two_weeks_later = current_date + timedelta(days=14)
        formatted_date = two_weeks_later.strftime('%Y-%m-%d')
        booking_date = formatted_date
        start_time = config.get('start_time')
        end_time = config.get('end_time')

        # Construct the booking URL with the desired date and times
        booking_url = (f'https://libcal.uflib.ufl.edu/spaces?m=t&lid=4316&gid=7502&'
                       f'capacity=0&date={booking_date}&date-end={booking_date}&start={start_time}&end={end_time}')

        # Navigate to the booking URL
        driver.get(booking_url)
        # time.sleep(1)
        # Wait for the list of available rooms to load
        wait = WebDriverWait(driver, 3)
        # Perform "Ctrl + F" to open the search bar
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'f')
        # Enter the search term into the search bar
        search_term = "L118 - Diode"
        search_input = driver.switch_to.active_element
        search_input.send_keys(search_term)

        # Press Enter to start the search
        search_input.send_keys(Keys.RETURN)
        book_now_button = driver.find_element(By.CLASS_NAME, 's-lc-suggestion-book-now')
        book_now_button.click()
        time.sleep(1)

        first_name_input = driver.find_element(By.ID, 'fname')
        first_name = config.get('first_name')
        first_name_input.send_keys(first_name)

        last_name_input = driver.find_element(By.ID, 'lname')
        last_name = config.get('last_name')
        last_name_input.send_keys(last_name)

        checkbox = driver.find_element(By.ID, 'terms')
        checkbox.click()
        # time.sleep(1)

        final_submit = driver.find_element(By.ID, 'btn-form-submit')
        final_submit.click()
        # Close the browser when done
        driver.quit()
