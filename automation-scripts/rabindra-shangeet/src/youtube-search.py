#!/usr/bin/env python

import time
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from helper.logger import *
from helper import logger

def youtube_in_new_tabs(search_queries, suffix, range_start, range_end, driver, delay, texts_to_find):
    """
    Opens YouTube in new browser tabs and searches for each query in the list.

    Args:
        search_queries (list): A list of strings, where each string is a search query.
    """
    if driver == 'Chrome':
        # Path to your ChromeDriver
        chrome_driver_path = '../out/chromedriver'

        # Set up the driver service
        service = Service(executable_path=chrome_driver_path)

        # Optional: Set options (e.g., maximize window)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # Launch Chrome with specified driver
        driver = webdriver.Chrome(service=service, options=options)

    else:

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

        tabs_to_be_closed = []

        for i, query in enumerate(search_queries[range_start:range_end]):
            if suffix != '':
                query = query + ' ' + suffix

            if i > 0:  # For subsequent queries, open a new tab
                # Open a new tab using JavaScript
                driver.execute_script("window.open('');")
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])
                driver.get("https://www.youtube.com/")
                print(i, f"Opened tab for query : '{query}'")
                time.sleep(2)  # Give the new tab some time to load

            # Find the search bar and perform the search
            try:
                search_bar = driver.find_element(By.NAME, "search_query")
                search_bar.clear()
                search_bar.send_keys(query)
                search_bar.send_keys(Keys.RETURN)
                print(i, f"Searching YouTube for: '{query}'")
                time.sleep(delay)  # Wait for search results to load
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


            # search for the provided text
            # Find all elements and check their text (more precise, good for user-visible text)
            # This is often more reliable as it looks at the *rendered* text content.
            # You can search for specific types of elements, like video titles, descriptions, etc.
            # Let's try to find it within all elements that are likely to contain video titles or descriptions.
            
            # Common elements that might contain relevant text:
            # 'yt-formatted-string' is a common YouTube custom element for text
            # 'h3' for video titles, 'div' or 'span' for descriptions

            found_in_element = False
            
            # Targeting specific elements where the text might appear
            # Example: Check video titles (h3 tag with specific ID/class)
            video_titles = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
            for title_element in video_titles[:4]:
                # print(f"... title [{title_element.text}]")
                # ignore some specific titles
                ignore = False
                for text in []:
                    if text in title_element.text:
                        ignore = True

                if True:
                    for text_item in texts_to_find:
                        if text_item.lower() in title_element.text.lower(): # Using .lower() for case-insensitivity
                            print(f"... '{text_item}' found in video title: {title_element.text}")
                            found_in_element = True
                            break # Stop after finding the first instance if you only need to confirm presence

                if found_in_element:
                    break

            if ignore:
                found_in_element = False
            
            if not found_in_element:
                # If not found in titles, maybe check descriptions or other text areas
                # You'll need to inspect the Youtube results page to find appropriate selectors
                # For instance, some description text might be in 'yt-formatted-string' elements
                description_elements = driver.find_elements(By.TAG_NAME, "yt-formatted-string")
                for desc_element in description_elements[:100]:
                    id = desc_element.get_attribute('id')
                    if id is None or id != 'corrected':
                        # print(f"... ... description [{desc_element.text}]")
                        for text_item in texts_to_find:
                            if text_item.lower() in desc_element.text.lower():
                                print(f"... '{text_item}' found in description/other text: {desc_element.text}")
                                print()
                                found_in_element = True
                                break

                    if found_in_element:
                        break
            
            if not found_in_element:
                print(f"... FIND terms not found in specific elements after search")
                print()
                tabs_to_be_closed.append(driver.current_window_handle)
                
        # close all tabs where find terms were not found
        print(f"Closing [{len(tabs_to_be_closed)}] tabs")
        for tab in tabs_to_be_closed:
            driver.switch_to.window(tab)
            driver.close()
        
            # found_any = False
            # for text_item in texts_to_find:
            #     for text_item in driver.page_source:
            #         print(f"Found '{text_item}' in page")
            #         found_any = True
            #         break

            #     # If you only need to know if *any* term is found in *this* text_item, you can break here
            #     if found_any:
            #         break

            # if found_any:
            #     print("... At least one search term was found in the list.")
            # else:
            #     print("... No search terms were found in the list.")


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # It's good practice to close the browser when done
        # time.sleep(10) # Uncomment this if you want to keep the browsers open for a bit to inspect
        # driver.quit()
        print("All searches completed. The browser remains open.")
        input("Press Enter to close...")

if __name__ == "__main__":

    # read config.yml
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)
    youtube_in_new_tabs(config.get('song-list', []), config.get('search-suffix', ''), config.get('range-start', ''), config.get('range-end', ''), config.get('driver', 'Chrome'), config.get('delay', 2), config.get('texts-to-find', []))