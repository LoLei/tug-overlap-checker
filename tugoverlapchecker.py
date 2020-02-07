#!/usr/bin/env python3
"""
TUG Overlap Checker
"""

__author__ = "Lorenz Leitner"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from requests_html import HTMLSession


def test():

    ## Selenium version
    url = "https://online.tugraz.at/tug_online/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/226888?$ctx=design=ca;lang=en;rbacId=&$scrollTo=toc_DatesandGroups"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1)
    page = driver.page_source
    print(page)
    soup = BeautifulSoup(page, 'html.parser')
    divs = soup.findAll("div", {"class": "compact-appointment"})
    print(divs)
    return

    ## RequestsHTML version
    url = "https://online.tugraz.at/tug_online/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/226888?$ctx=design=ca;lang=en;rbacId=&$scrollTo=toc_DatesandGroups"
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(str(r.html), 'lxml')
    print(r.html.text)
    divs = soup.findAll("div", {"class": "compact-appointment"})
    print(divs)
    return


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("classid", help="class id")
    return parser.parse_args()


def main():
    args = parse_args()
    test()


if __name__ == "__main__":
    main()
