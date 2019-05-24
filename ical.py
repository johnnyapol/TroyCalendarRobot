'''
Created on Jun 26, 2018

@author: john
'''

import urllib.request

from datetime import datetime

from event_calendar import Date


class CalendarManager():

    def __init__(self):
        pass

    @staticmethod
    def download_calendar_file(link, calendar):
        urllib.request.urlretrieve(link, calendar)

    @staticmethod
    def get_date_string():
        return str(datetime.today())

    @staticmethod
    def get_year():
        return CalendarManager.get_date_string()[0:4]

    @staticmethod
    def get_month():
        return CalendarManager.get_date_string()[5:7]

    @staticmethod
    def get_day():
        return int(CalendarManager.get_date_string()[8:10])

    @staticmethod
    def get_month_int(month):
        return int(month)

    @staticmethod
    def get_today():
        return Date(CalendarManager.get_month_int(CalendarManager.get_month()), CalendarManager.get_day(), int(CalendarManager.get_year()))
