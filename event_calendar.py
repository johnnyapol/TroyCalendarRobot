'''
Created on Jun 26, 2018

@author: john
'''

from icalendar import Calendar

DEBUG = False

# Month End Table
MONTH_MAX = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class EventCalendar:

    def __init__(self, file):
        self.file = file

    def parseEvents(self):
        cal = Calendar.from_ical(open(self.file).read())

        events = []
        for event in cal.walk():
            # Time to shine
            if event.name == "VEVENT":
                if DEBUG:
                    print(event)
                    print(event.decoded('dtstart'))
                    print("******* EVENT *******")
                    print("SUMMARY: " + event.get('summary'))
                    print("DESCRIPTION: " + event.get('description'))
            #       print ("START: " + str(cal.decoded(event.get('dtstart'))))
                    print("END: " + str(event.get('dtend')))
                    print("TIMESTAMP: " + str(event.get('dtstamp')))
                    print("ADDRESS: " + event.get('LOCATION'))
                    print("************************")

                calEvent = CalEvent(event.get('summary'), event.decoded(
                    'dtstart'), event.get('description'), event.get('LOCATION'))

                events.append(calEvent)
        # Return dictionary of events
        return events


class CalEvent:
    def __init__(self, summary, start, description, address=None):
        self.summary = summary
        self.description = description
        self.address = address

        # Fix time
        self.start = start

    def get_summary(self):
        return self.summary

    def get_start(self):
        return self.start

    def get_description(self):
        return self.description

    def get_address(self):
        return self.address


class Date:
    # Input: MM/DD/YYYYY in integer format
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    # Returns true if the two date objects are the same
    def equals(self, other_date):
        #print("Comparing: [" + str(self.month) + "/" + str(self.day) + "/" + str(self.year) + "] with [" + str(other_date.month) + "/" + str(other_date.day) + "/" + str(other_date.year) + "]\n")
        return (other_date.day == self.day and other_date.month == self.month and other_date.year == self.year)

    # Returns the month the date corresponds to
    # 1 = January, 2 = February, ......, 12 = December

    def get_month(self):
        return self.month

    # Returns the day that the date corresponds to
    def get_day(self):
        return self.day

    # Returns the year that the date corresponds to
    def get_year(self):
        return self.year

    # Constructs a date object corresponding to the next day
    # in the calendar year

    def get_tomorrow(self):
        # Grab the end of month
        end_of_month = MONTH_MAX[self.month - 1]

        # Prepare vars for our new date object
        next_day = self.day + 1
        next_month = self.month
        next_year = self.year

        # See if we're in february and apply leap year rules
        if (self.month - 1 is 1):
            leap_year = ((self.year % 4 == 0 and self.year %
                          100 is not 0) or year % 400 is 0)
            end_of_month += (1 if leap_year else 0)

        # See if we're at the end of the month
        if (self.day is end_of_month):
            next_day = 1
            next_month += 1

        # We index months as January = 1, December = 12
        # So we need to overflow into a new year!
        if (next_month is 13):
            next_month = 1
            next_year += 1

        # Construct new date object!
        print("Today: " + str(self.month) + "/" +
              str(self.day) + "/" + str(self.year) + "\n")
        print("Tomorrow: " + str(next_month) + "/" +
              str(next_day) + "/" + str(next_year) + "\n")
        return Date(next_month, next_day, next_year)
