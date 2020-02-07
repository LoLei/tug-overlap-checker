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
from datetime import datetime


class Appointment:
    def __init__(self, date_str, time_range_str):
        print(date_str)
        self.date_ = datetime.strptime(date_str.strip(), '%d.%m.%Y').date()
        self.time_range_ = time_range_str.replace(' ', '').split('-')
        self.start_time_ = self.time_range_[0]
        self.end_time_ = self.time_range_[1]


def get_overlaps():
    url = "https://online.tugraz.at/tug_online/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/226888?$ctx=design=ca;lang=en;rbacId=&$scrollTo=toc_DatesandGroups"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    divs = soup.find_all("div", class_="compact-appointment-info")

    appointments = []
    for div in divs:
        date_str = div.find("span", class_="appointment-date").text
        date_str = date_str[len(" on "):]

        time_range_str = div.find("span", class_="appointment-time").text
        time_range_str = time_range_str[len(", "):]

        appointment = Appointment(date_str, time_range_str)
        appointments.append(appointment)

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
    # Note: The comparison of n classes is most likely in O(n^2)
    # however it can be optimized by comparing only in one direction.
    # E.g. if day 1 and day 3 have been compared, day 3 and day 1 need not be
    # compared
    get_overlaps()


if __name__ == "__main__":
    main()
