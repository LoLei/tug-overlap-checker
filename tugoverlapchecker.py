#!/usr/bin/env python3
"""
TUG Overlap Checker
"""

__author__ = "Lorenz Leitner"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import time
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver


def test():
    url = "https://online.tugraz.at/tug_online/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/226888?$ctx=design=ca;lang=en;rbacId=&$scrollTo=toc_DatesandGroups"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    divs = soup.findAll("div", {"class": "compact-appointment-info"})
    print(divs)

    # TODO:
    # 1. Check if conflicting dates
    # 2. Check if conflicting times on conflicting dates
    #
    # Range overlap check:
    # 1. Get highest start value and lowest end value
    # 2. Subtract
    # 3. If delta is positive: Overlap
    # For dates: https://stackoverflow.com/a/9044111/4644044



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("classid", help="class id")
    return parser.parse_args()


def main():
    args = parse_args()
    test()


if __name__ == "__main__":
    main()
