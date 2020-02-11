# tug-overlap-checker

Check for course overlaps at Graz University of Technology 🎓

The tool will get the dates and times for specified courses,
compare them, and report any conflicts.

## Installation
`pip install tug-overlap-checker`

## Usage
```
$ tug-overlap-checker -h
usage: tug-overlap-checker [-h] courseid [courseid ...]

positional arguments:
  courseid    course ids

optional arguments:
  -h, --help  show this help message and exit
```

The `courseid` argument can be repeated to specify multiple.
This is the ID that is found in the URL of TUGO, **not**
the visually displayed class ID. This may be changed in the
future so the conventional IDs can be used.

E.g.:  
`https://online.tugraz.at/tug_online/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/xxxxxx` <--

### Example Usage
```
$ tug-overlap-checker 226888 221424 225088
Found course: Information and Communication Management, with 3 appointments.
Appointment: date: 2020-06-17, time range: ['13:30', '21:00']
Appointment: date: 2020-06-18, time range: ['09:30', '20:00']
Appointment: date: 2020-06-19, time range: ['08:00', '14:00']

Found course: Entrepreneurship, with 6 appointments.
Appointment: date: 2020-04-01, time range: ['14:00', '17:30']
Appointment: date: 2020-05-04, time range: ['09:00', '18:00']
Appointment: date: 2020-05-05, time range: ['09:00', '18:00']
Appointment: date: 2020-05-06, time range: ['09:00', '18:00']
Appointment: date: 2020-05-07, time range: ['09:00', '18:00']
Appointment: date: 2020-05-08, time range: ['09:00', '18:00']

Found course: Marketing Management, with 7 appointments.
Appointment: date: 2020-04-27, time range: ['12:00', '12:45']
Appointment: date: 2020-05-04, time range: ['09:00', '18:00']
Appointment: date: 2020-05-07, time range: ['08:15', '15:00']
Appointment: date: 2020-05-11, time range: ['08:15', '18:00']
Appointment: date: 2020-05-13, time range: ['08:15', '15:00']
Appointment: date: 2020-05-18, time range: ['08:15', '18:00']
Appointment: date: 2020-05-20, time range: ['08:15', '15:00']

Comparing "Information and Communication Management" and "Entrepreneurship"...
No date overlap.
Comparing "Information and Communication Management" and "Marketing Management"...
No date overlap.
Comparing "Entrepreneurship" and "Marketing Management"...
Found date overlap.
Conflicting dates:
2020-05-07
2020-05-04
Checking for time overlap on "2020-05-07"...
Times to check: ['09:00', '18:00'], ['08:15', '15:00']
Found time overlap.
For courses Entrepreneurship and Marketing Management on 2020-05-07
Checking for time overlap on "2020-05-04"...
Times to check: ['09:00', '18:00'], ['09:00', '18:00']
Found time overlap.
For courses Entrepreneurship and Marketing Management on 2020-05-04
```

## Background
Due to many conflicting classes this semester and seeing how
comparing them manually is a PITA, this tool was created to
automate the process.

Since many different universities use the same online system,
this may very well also work with other universities' sites
like KFU. Changing the access URL is necessary for this though.

Unfortunately there is no API for TUGO, or at least none that 
is easily accessible for a small project like this (since Studo
*must* have one), therefore the data is scraped from the website
at [generous intervals](https://online.tugraz.at/robots.txt).
