#!/usr/bin/env python3
"""
TUG Overlap Checker
"""

__author__ = "Lorenz Leitner"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from textwrap import dedent
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime


class Appointment:
    def __init__(self, date_str, time_range_str):
        self.date_ = datetime.strptime(date_str.strip(), '%d.%m.%Y').date()
        self.time_range_ = time_range_str.replace(' ', '').split('-')
        self.start_time_ = self.time_range_[0]
        self.end_time_ = self.time_range_[1]

    def __str__(self):
        return "Appointment: date: {}, time range: {}".format(
            self.date_, self.time_range_)

    def __eq__(self, other):
        if isinstance(other, Appointment):
            return self.date_ == other.date_
        return False

    def __hash__(self):
        return hash(self.date_)


class Course:
    def __init__(self, course_id):
        self.appointments_ = []
        self.course_title_ = ""

        url = """
        https://online.tugraz.at/
        tug_online/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/
        {course_id}
        ?$ctx=design=ca;lang=en;rbacId=
        &$scrollTo=toc_DatesandGroups
        """.format(course_id=course_id)
        url = dedent(url).replace('\n', '')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1920x1080')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        self.course_title_ = soup.find("span",
                                       class_="ca-header-page-title").text[len(
                                           "Courses / "):]

        # Get all appointment elements
        divs = soup.find_all("div", class_="compact-appointment-info")

        for div in divs:
            date_str = div.find("span", class_="appointment-date").text
            date_str = date_str[len(" on "):]

            time_range_str = div.find("span", class_="appointment-time").text
            time_range_str = time_range_str[len(", "):]

            appointment = Appointment(date_str, time_range_str)
            self.appointments_.append(appointment)

        print("Found course: {}, with {} appointments.".format(
            self.course_title_,
            len(self.appointments_)))

    def get_dates(self):
        dates = []
        for appointment in self.appointments_:
            dates.append(appointment.date_)
        return dates

    def print_appointments(self):
        for appointment in self.appointments_:
            print(appointment)


def compare_appointments(appointment1, appointment2):
    """
    Compare two appointments on the same day
    """
    assert appointment1.date_ == appointment2.date_
    print("Checking for time overlap on \"{}\"...".
          format(appointment1.date_))
    # TODO


def compare_courses(course1, course2):
    """
    Compare two different courses
    """
    print("Comparing \"{}\" and \"{}\"...".format(
        course1.course_title_, course2.course_title_))

    # First check conflicting dates
    latest_start = max(course1.appointments_[0].date_,
                       course2.appointments_[0].date_)

    earliest_end = min(course1.appointments_[len(
                        course1.appointments_) - 1].date_,
                       course2.appointments_[len(
                        course2.appointments_) - 1].date_)

    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)
    if overlap == 0:
        print("No date overlap.")
        return

    print("Found date overlap.")

    # Find exact overlapping days
    conflicting_appointments = list(
        set(course1.appointments_) & set(course2.appointments_))
    print("Conflicting dates:")
    for c_a in conflicting_appointments:
        print(c_a.date_.strftime('%Y-%m-%d'))

    for c_a in conflicting_appointments:
        compare_appointments(
            course1.appointments_[course1.appointments_.index(c_a)],
            course2.appointments_[course2.appointments_.index(c_a)])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('courseid', help="course ids", nargs='+')
    return parser.parse_args()


def main():
    # Note: The comparison of n courses is most likely in O(n^2)
    # however it can be optimized by comparing only in one direction.
    # E.g. if day 1 and day 3 have been compared, day 3 and day 1 need not be
    # compared

    args = parse_args()

    # Supply these via input argument
    # Also maybe get these via search of the actual course ID
    # (xxx.xxx)
    # course_ids = [226888, 221424, 225088]
    course_ids = args.courseid
    courses = []
    for course_id in course_ids:
        course = Course(course_id)
        courses.append(course)
        course.print_appointments()
        print()

    compare_courses(courses[1], courses[2])


if __name__ == "__main__":
    main()
