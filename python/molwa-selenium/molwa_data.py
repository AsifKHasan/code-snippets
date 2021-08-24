#!/usr/bin/env python3

from selenium import webdriver

URL = 'http://mis.molwa.gov.bd/freedom-fighter-list?division_id={0}&page={1}'
DIVISION = (7, 'SYLHET', 1173)

def init():
    browser = webdriver.Firefox()
    # browser.maximize_window()
    browser.implicitly_wait(0)
    return browser

def load(browser, url):
    try:
        browser.get(url)
    except Exception as e:
        raise(e)

    names = [name.get_attribute("innerHTML") for name in browser.find_elements_by_xpath("//table[@class='table table-bordered']/tbody/tr/td[3]")]
    father_names = [name.get_attribute("innerHTML") for name in browser.find_elements_by_xpath("//table[@class='table table-bordered']/tbody/tr/td[4]")]
    
    return names, father_names

if __name__ == '__main__':
    browser = init()

    # 4 is Khulna division, each page contains 10 rows
    all_names, all_father_names = [], []
    for page in range(1, DIVISION[2]):
        url = URL.format(DIVISION[0], page)
        try:
            names, father_names = load(browser, url)
            all_names = all_names + names
            all_father_names = all_father_names + father_names
            print('pages done {0}'.format(page))
        except Exception as e:
            print(e)
            break

    file_name = '{0}__freedom-fighters.txt'.format(DIVISION[1])
    with open(file_name, 'a') as f:
        f.write('\n'.join(all_names))
        f.write('\n'.join(all_father_names))