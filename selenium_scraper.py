import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service  # Import the Service class

BASE_URL = 'https://travel.state.gov'

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

# Initialize the chromediver (must be installed and in PATH)
# Needed to implement the headless option
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

def get_wait_time(driver, city_name):
    '''Scrapes the visa appointment wait time for the given city.'''
    print(f"Fetching wait time for {city_name}.")

    # Open the wait times page
    driver.get(BASE_URL + '/content/travel/en/us-visas/visa-information-resources/wait-times.html')

    time.sleep(5)  # Allow time for the page to fully load

    try:
        # Confirm page has loaded properly
        print("Page title:", driver.title)

        # Find the search box and enter the city name (Addis Ababa)
        search_box = driver.find_element(By.ID, 'search_input')  
        search_box.clear()
        search_box.send_keys(city_name)

        print(f"Searching for {city_name}...")

        # Wait for the search to process
        time.sleep(5)

        # Scrape the result that shows the wait time for Nonimmigrant Visa
        wait_time_element = driver.find_element(By.XPATH, "//td[contains(text(),'Addis Ababa')]/following-sibling::td[1]")  # Adjust the XPath based on actual page structure
        wait_time = wait_time_element.text
        print(f"Visa appointment wait time for {city_name}: {wait_time}")
        return wait_time

    except NoSuchElementException as e:
        print(f"Could not find the required element: {e}")
        return None

def run_visa_scraper(city_name):
    # Setting Chrome options to run the scraper headless.
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment this line to run headless

    # Initialize the ChromeDriver using Service
    chrome_service = Service('/path/to/chromedriver')  # Specify the path to chromedriver

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        wait_time = get_wait_time(driver, city_name)

        if wait_time:
            print('A change was found or wait time retrieved. Notifying it.')
            # send_message(f'Visa appointment wait time for {city_name}: {wait_time}')
        else:
            print('No relevant wait time found.')

    finally:
        driver.quit()  # Ensure the browser is closed

def main():
    city_name = 'Addis Ababa'  # City for which to check the visa wait time
    run_visa_scraper(city_name)

if __name__ == "__main__":
    main()
