#!/usr/bin/env python

import time
import yaml
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from helper.logger import *
from helper import logger

def new_tabs(config):
    links_to_open = config.get('links-to-open', [])
    range_start = config.get('range-start', '')
    range_end = config.get('range-end', '')
    search_patterns = config.get('texts-to-find', [])
    web_driver = config.get('driver', 'Chrome')
    delay_link_load = config.get('delay-link-load', 1)
    delay_link_tab = config.get('delay-yt-tab', 1)

    if web_driver == 'Chrome':
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

    outputs = []
    try:
        time.sleep(delay_link_load)  # Give the page some time to load

        for i, link in enumerate(links_to_open[range_start:range_end]):

            if i > 0:  # For subsequent links, open a new tab
                # Open a new tab using JavaScript
                driver.execute_script("window.open('');")
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

            driver.get(link)
            info(f"[{i}] Opened tab for: '{link}'")
            # Give the new tab some time to load
            time.sleep(delay_link_load)

            # 1. Get the full page source
            page_source = driver.page_source

            match_found = False
            for search_pattern in search_patterns:
                matches_in_page = re.findall(search_pattern, page_source)

                if matches_in_page:
                    for found_text in matches_in_page:
                        debug(f"[{found_text}] found in page source:")
                        outputs.append((link, found_text))
                        match_found = True
                        break

            if not match_found:
                    outputs.append((link, ''))
                    warn(f"no search_pattern found in page source.")            

    except Exception as e:
        error(f"An error occurred: {e}")
    finally:
        debug("All links completed. The browser remains open.")
        for output in outputs:
            print(output[0], output[1])

        input("Press Enter to close...")

if __name__ == "__main__":

    # read config.yml
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)
    new_tabs(config)