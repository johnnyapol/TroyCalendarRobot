'''
Created on Jun 26, 2018

@author: john
'''

import urllib.request

from datetime import datetime

class CalendarManager():
    
    def __init__(self):
        pass
    
    
    @staticmethod
    def downloadCalendarFile(link, calendar):
        urllib.request.urlretrieve(link, calendar)
        
    
    
    @staticmethod
    def getDateString():
        return str(datetime.today())
    
    @staticmethod
    def getYear():
        return CalendarManager.getDateString()[0:4]
    
    @staticmethod
    def getMonth():
        return CalendarManager.getDateString()[5:7]
    
    @staticmethod
    def getDay():
        return int(CalendarManager.getDateString()[8:10])