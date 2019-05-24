'''
Created on Jun 26, 2018

@author: john
'''

from icalendar import Calendar

class EventCalendar:
    
    def __init__(self, file):
        self.file = file
    
    def parseEvents(self):
        cal = Calendar.from_ical(open(self.file).read())
        
        events = [ ]
        for event in cal.walk():
            print(event)
            # Time to shine
            if event.name == "VEVENT":
                print(event.decoded('dtstart'))
                print ("******* EVENT *******")
                print ("SUMMARY: " + event.get('summary'))
                print ("DESCRIPTION: " + event.get('description'))
            #    print ("START: " + str(cal.decoded(event.get('dtstart'))))
                print ("END: " + str(event.get('dtend')))
                print ("TIMESTAMP: " + str(event.get('dtstamp')))
                print ("ADDRESS: " + event.get('LOCATION'))
                print ("************************")
        
        
                calEvent = CalEvent(event.get('summary'), event.decoded('dtstart'), event.get('description'), event.get('LOCATION'))
                
                events.append(calEvent)
        # Return dictionary of events
        return events
        
    
class CalEvent: 
    def __init__(self, summary, start, description, address = None):
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
    