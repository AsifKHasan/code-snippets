#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

search_suffix = ' দেবব্রত বিশ্বাস'
my_search_list = [
]

def youtube_in_new_tabs(search_queries):
    """
    Opens YouTube in new browser tabs and searches for each query in the list.

    Args:
        search_queries (list): A list of strings, where each string is a search query.
    """
    # # Path to your ChromeDriver
    # chrome_driver_path = '../out/chromedriver'

    # # Set up the driver service
    # service = Service(executable_path=chrome_driver_path)

    # # Optional: Set options (e.g., maximize window)
    # options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")

    # # Launch Chrome with specified driver
    # driver = webdriver.Chrome(service=service, options=options)


    # Path to your FirefoxDriver
    firefox_driver_path = '../out/geckodriver'

    # Set up the driver service
    service = Service(executable_path=firefox_driver_path)

    # Optional: Set options (e.g., maximize window)
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")

    # Launch Chrome with specified driver
    driver = webdriver.Firefox(service=service, options=options)


    try:
        # Open the first YouTube tab
        driver.get("https://www.youtube.com/")
        print("Opened YouTube in the first tab.")
        time.sleep(2)  # Give the page some time to load

        for i, query in enumerate(search_queries):
            query = query + search_suffix
            if i > 0:  # For subsequent queries, open a new tab
                # Open a new tab using JavaScript
                driver.execute_script("window.open('');")
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])
                driver.get("https://www.youtube.com/")
                print(f"Opened new tab for query: '{query}'")
                time.sleep(2)  # Give the new tab some time to load

            # Find the search bar and perform the search
            try:
                search_bar = driver.find_element(By.NAME, "search_query")
                search_bar.clear()
                search_bar.send_keys(query)
                search_bar.send_keys(Keys.RETURN)
                print(f"Searching YouTube for: '{query}'")
                time.sleep(3)  # Wait for search results to load
            except Exception as e:
                print(f"Could not find search bar or perform search for '{query}': {e}")
                # If search bar not found, try to go to YouTube home and retry
                driver.get("https://www.youtube.com/")
                time.sleep(2)
                try:
                    search_bar = driver.find_element(By.NAME, "search_query")
                    search_bar.clear()
                    search_bar.send_keys(query)
                    search_bar.send_keys(Keys.RETURN)
                    print(f"Retrying search for: '{query}'")
                    time.sleep(3)
                except Exception as e_retry:
                    print(f"Retry failed for '{query}': {e_retry}")


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # It's good practice to close the browser when done
        # time.sleep(10) # Uncomment this if you want to keep the browsers open for a bit to inspect
        # driver.quit()
        print("All searches completed. The browser remains open.")
        input("Press Enter to close...")

if __name__ == "__main__":

    youtube_in_new_tabs(my_search_list)