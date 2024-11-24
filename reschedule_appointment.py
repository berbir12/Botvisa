import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_scraper import log_in
from telegram import send_message, send_photo

url = 'https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/wait-times.html/'

# Setting Chrome options to run the scraper headless.
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

# Initialize the chromediver (must be installed and in PATH)
# Needed to implement the headless option
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


def check_for_appointments():
    '''Checks for changes in the calendar. Returns True if a change was found.'''
    try:
        # First website
        driver.get(url)

        # Logging in
        log_in(driver)  # Pass the driver to the log_in function

        print('Navigating to the calendar page.')
        
        # Locate and click the input button to open the calendar
        input_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'appointments_consulate_appointment_date'))
        )
        input_button.click()

        
        time.sleep(2)

        def check_calendar():
            print('Checking the calendar for active dates.')
            # Locate the calendar element
            calendar_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-calendar'))
            )
            # Find all active date elements (assuming active dates have no 'ui-datepicker-unselectable' class)
            active_dates = calendar_element.find_elements(By.XPATH, ".//td[not(contains(@class, 'ui-datepicker-unselectable'))]")
            return active_dates

        # Check the current month
        if check_calendar():
            print("Active dates found in the current month.")
            send_message('Active dates found in the current month.')
            screenshot_path = 'screenshot.png'
            driver.save_screenshot(screenshot_path)
            send_photo(screenshot_path)
            return True

        
        

        print("No active dates found in the current.")
        return False
    except Exception as e:
        print(f'An error occurred: {e}')
        return False



def repeat_check(seconds_between_checks):
    '''A function that calls the checking function in a given interval of time'''
    try:
        while True:
            current_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
            print(f'Starting a new check at {current_time}.')
            if check_for_appointments():
                print('A change was found. Notifying it.')
                break  # Exit the loop after finding a change
            else:
                send_message('No change was found.')
                screenshot_path = 'screenshot.png'
                driver.save_screenshot(screenshot_path)
                send_photo(screenshot_path)
                for seconds_remaining in range(int(seconds_between_checks), 0, -1):
                    sys.stdout.write('\r')
                    sys.stdout.write(
                        f'No change was found. Checking again in {seconds_remaining} seconds.'
                    )
                    sys.stdout.flush()
                    time.sleep(1)
                print('\n')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        driver.quit()  # Ensure the driver quits properly


if __name__ == "__main__":
    repeat_check(seconds_between_checks=10*60)