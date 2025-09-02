#!/usr/bin/env python

import time
import yaml
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helper.logger import *
from helper import logger

def init(driver, url):
    if driver == 'Chrome':
        # Path to your ChromeDriver
        chrome_driver_path = '../out/chromedriver'

        # Set up the driver service
        service = Service(executable_path=chrome_driver_path)

        # Optional: Set options (e.g., maximize window)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # Launch Chrome with specified driver
        browser = webdriver.Chrome(service=service, options=options)

    else:
        # Path to your FirefoxDriver
        firefox_driver_path = '../out/geckodriver'

        # Set up the driver service
        service = Service(executable_path=firefox_driver_path)

        # Optional: Set options (e.g., maximize window)
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")

        # Launch Chrome with specified driver
        browser = webdriver.Firefox(service=service, options=options)

    try:
        browser.get(url)
    except Exception as e:
        raise(e)

    return browser


def extract_courts(browser):
    # get the date
    date_input = browser.find_element('xpath', '//input[@id="date1"]')
    date_str = date_input.get_attribute("value")
    court_date = datetime.strptime(date_str, '%d/%m/%Y')

    tr_elements = browser.find_elements('xpath', "//table[@class='link_e10r']/tbody/tr")
    # trs = [tr.get_attribute("innerHTML") for tr in browser.find_element('xpath', "//table[@class='link_e10r']/tbody/tr")]
    court_list = []
    for i, tr_element in enumerate(tr_elements[1:], start=1):
        td_elements = tr_element.find_elements(By.TAG_NAME, "td")

        # there are four columns
        assert len(td_elements) == 4
        court_sl = td_elements[0].text.strip()

        court_td = td_elements[1]
        court_texts = td_elements[1].text.split('\n')
        # court_text has three lines
        # assert len(court_texts) == 4
        # Extract text from each cell
        court_name = court_texts[0].strip()
        # now cases and results
        cases, results = None, None
        for line in court_texts[1:]:
            if 'Total cases : ' in line:
                cases = int(line.replace('Total cases : ', ''))

            if 'Result given : ' in line:
                results = int(line.replace('Result given : ', ''))

        # court url
        court_url_a = court_td.find_element(By.TAG_NAME, "a")
        court_url = court_url_a.get_attribute("href")

        court_list.append({'court-sl': court_sl, 'court-name': court_name, 'court-url': court_url, 'total-cases': cases, 'results-given': results})

    return court_list, court_date


def extract_cause_list(browser, court_sl, court_name, court_url, cases, results):
    info(f"  processing cause list .. {court_sl}. {court_name}")
    try:
        browser.get(court_url)
        time.sleep(2)

    except Exception as e:
        raise(e)

    tr_elements = browser.find_elements('xpath', "//table[@class='friend']/tbody/tr")
    # only trs with 4 td's are to be considered
    cause_list = []
    for tr_element in tr_elements:
        td_elements = tr_element.find_elements(By.TAG_NAME, "td")
        # print(f"{td_elements[0].text.strip()}, length {len(td_elements)}")

        if len(td_elements) >= 4:
            cause_sl = td_elements[0].text.strip()
            # print(cause_sl)
            if cause_sl == 'Sl':
                continue
            
            case_number_lines = td_elements[1].text.split('\n')
            parties_lines = td_elements[2].text.split('\n')

            cause_list.append({'cause-sl': cause_sl, 'case-number-text': case_number_lines, 'parties-text': parties_lines})

    return cause_list


def curate_cause_list(cause_list, case_search_list, party_search_list):
    curated_cause_list = []
    for i, cause in enumerate(cause_list, start=1):
        cause_sl, case_number_lines, parties_lines = cause.values()
        one_case_search_failed = False
        for term in case_search_list:
            case_search_found = any(term in line for line in case_number_lines)
            if not case_search_found:
                one_case_search_failed = True

        if not one_case_search_failed:
            party_search_found = any(text.lower() in line.lower() for line in parties_lines for text in party_search_list)
            if party_search_found:
                curated_cause_list.append(cause)

    return curated_cause_list


def output_to_file(courts, court_date, output_dir, range_start, range_end):
    lines = []
    for i, court in enumerate(courts[range_start:range_end], start=1):
        court_sl, court_name, court_url, cases, results = court['court-sl'], court['court-name'], court['court-url'], court['total-cases'], court['results-given']
        cause_list, curated_cause_list = court.get('cause-list', []), court.get('curated-cause-list', [])

        if len(curated_cause_list) == 0:
            continue

        lines.append(f"court serial {court_sl}")
        lines.append(f"  Court         : {court_name}")
        lines.append(f"  URL           : {court_url}")
        lines.append(f"  Total Cases   : {cases}")
        lines.append(f"  Curated Cases : {len(curated_cause_list)}")
        lines.append(f"  ---------------")

        for j, cause in enumerate(curated_cause_list, start=1):
            cause_sl, case_number_lines, parties_lines = cause.values()
            lines.append(f"    Cause Sl     : {cause_sl}")

            for k, line in enumerate(case_number_lines):
                if k == 0:
                    lines.append(f"    Cause number : {line}")
                else:
                    lines.append(f"                   {line}")

            for k, line in enumerate(parties_lines):
                if k == 0:
                    lines.append(f"    Parties      : {line}")
                else:
                    lines.append(f"                   {line}")

            lines.append('')

        lines.append('')

    file_name = f"{output_dir}court-cause-list__{court_date.strftime('%Y-%m-%d')}.txt"
    with open(file_name, 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    # read config.yml
    config = yaml.load(open('../conf/config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
    logger.LOG_LEVEL = config.get('log-level', 0)
    driver = config.get('driver', 'Firefox')
    output_dir = config.get('output-dir', None)
    root_url = config.get('root-url', None)
    case_search_list = config.get('case-search-list', [])
    party_search_list = config.get('party-search-list', [])
    range_start = config.get('range-start', 0)
    range_end = config.get('range-end', '')

    browser = init(driver=driver, url=root_url)

    courts, court_date = extract_courts(browser)
    info(f"{len(courts)} courts found, date {court_date.strftime('%Y-%m-%d')}")
    for i, court in enumerate(courts[range_start:range_end], start=1):
        court_sl, court_name, court_url, cases, results = court.values()
        debug(f"court serial {court_sl}")
        debug(f"  Court   : {court_name}")
        debug(f"  URL     : {court_url}")
        debug(f"  Cases   : {cases}")
        debug(f"  Results : {results}")

        cause_list = extract_cause_list(browser=browser, court_sl=court_sl, court_name=court_name, court_url=court_url, cases=cases, results=results)
        info(f"  {len(cause_list)} causes found")
        if len(cause_list) != cases:
            warn(f"  expected {cases} causes, found {len(cause_list)} causes")

        for i, cause in enumerate(cause_list, start=1):
            cause_sl, case_number_lines, parties_lines = cause.values()
            trace(f"    Cause Sl     : {cause_sl}")

            for k, line in enumerate(case_number_lines):
                if k == 0:
                    trace(f"    Cause number : {line}")
                else:
                    trace(f"                   {line}")

            for k, line in enumerate(parties_lines):
                if k == 0:
                    trace(f"    Parties      : {line}")
                else:
                    trace(f"                   {line}")

        court['cause-list'] = cause_list

        # now curate the cause list
        curated_cause_list = curate_cause_list(cause_list=cause_list, case_search_list=case_search_list, party_search_list=party_search_list)
        info(f"  {len(curated_cause_list)} curated causes found")
        court['curated-cause-list'] = curated_cause_list

        for i, cause in enumerate(curated_cause_list, start=1):
            cause_sl, case_number_lines, parties_lines = cause.values()
            debug(f"    Cause Sl     : {cause_sl}")

            for k, line in enumerate(case_number_lines):
                if k == 0:
                    debug(f"    Cause number : {line}")
                else:
                    debug(f"                   {line}")

            for k, line in enumerate(parties_lines):
                if k == 0:
                    debug(f"    Parties      : {line}")
                else:
                    debug(f"                   {line}")

    output_to_file(courts=courts, court_date=court_date, output_dir=output_dir, range_start=range_start, range_end=range_end)
