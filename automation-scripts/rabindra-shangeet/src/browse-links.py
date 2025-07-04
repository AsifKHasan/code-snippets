#!/usr/bin/env python

import time
import yaml

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from helper.logger import *
from helper import logger

def new_tabs(config):
    links_to_open = config.get('links-to-open', [])
    range_start = config.get('range-start', '')
    range_end = config.get('range-end', '')
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

                
    except Exception as e:
        error(f"An error occurred: {e}")
    finally:
        debug("All links completed. The browser remains open.")
        input("Press Enter to close...")

if __name__ == "__main__":

    # read config.yml
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)
    new_tabs(config)