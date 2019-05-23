'''
Created on Jun 26, 2018

@author: john
'''
from rcalendar import EventCalendar
from ical import CalendarManager
from reddit import RedditManager

def __init__():
    # Download links to /r/Troy .ics files from the google calendars
    TROY_ART = "https://calendar.google.com/calendar/ical/a7hd2r4rrosgqnmeq3rlgnfrg0%40group.calendar.google.com/public/basic.ics"
    TROY_FESTIVALS = "https://calendar.google.com/calendar/ical/4a0bfik43rli6v4qhr2lp6nh6k%40group.calendar.google.com/public/basic.ics"
    #TROY_KIDS = "https://calendar.google.com/calendar/ical/5qneb2ti8iuevupniijsibusdo%40group.calendar.google.com/public/basic.ics"
    TROY_MUSIC = "https://calendar.google.com/calendar/ical/s83fkkrfbsks0mph5k836nsmhs%40group.calendar.google.com/public/basic.ics"
    TROY_OTHER = "https://calendar.google.com/calendar/ical/go2vrfg91b62mvglq3hqu45pnc%40group.calendar.google.com/public/basic.ics"
    
    # Download rcalendar files
    print("Downloading rcalendar files...")
    CalendarManager.downloadCalendarFile(TROY_ART, "art.ics")
    CalendarManager.downloadCalendarFile(TROY_FESTIVALS, "festivals.ics")
    #CalendarManager.downloadCalendarFile(TROY_KIDS, "kids.ics")
    CalendarManager.downloadCalendarFile(TROY_MUSIC, "music.ics")
    CalendarManager.downloadCalendarFile(TROY_OTHER, "other.ics")
    
    
    # Begin parsing
    artCal = EventCalendar("art.ics")
    artEvents = artCal.parseEvents()
    
    del artCal
    
    festivalsCal = EventCalendar("festivals.ics")
    festivalEvents = festivalsCal.parseEvents()
    
    del festivalsCal
    
    #kidsCal = EventCalendar("kids.ics")
    #kidsEvents = kidsCal.parseEvents()
    
    #del kidsCal
    
    musicCal = EventCalendar("music.ics")
    musicEvents = musicCal.parseEvents()
    
    otherCal = EventCalendar("other.ics")
    otherEvents = otherCal.parseEvents()
    
    del otherCal
    
    # Prepare post
    text = 'Hello! Here are the Troy events for this week, organized by category. \n\n# Art Events\n\n******'
    
    aEvents = computeEvents(artEvents)
    fEvents = computeEvents(festivalEvents)
    #kEvents = computeEvents(kidsEvents)
    mEvents = computeEvents(musicEvents)
    oEvents = computeEvents(otherEvents)
    
    text += parseEvents(aEvents)
    text += "\n\n# Festival Events\n\n******"
    text += parseEvents(fEvents) 
    #text += "\n\n# Kids Events\n\n******"
    #text += parseEvents(kEvents) 
    text += "\n\n# Music Events\n\n******"
    text += parseEvents(mEvents) 
    text += "\n\n# Other Events\n\n******"
    text += parseEvents(oEvents)
    
    text += "\nI am a bot, and this action was performed automatically."
    
    print (text)
    
    f = open("log.txt", 'w')
    
    f.write(text)
    
    reddit = setupReddit()
    # Post to reddit
    post = reddit.post("Troy", "Weekly Events for " + CalendarManager.getMonth() + "/" + str(CalendarManager.getDay()) + "/" + CalendarManager.getYear(), text)
    reddit.crosspost(post, "rpi")
    
def setupReddit():
    # Find credential file
    creds = open('reddit.cfg', 'r')
    
    data = creds.readlines()
    
    cId = ''
    cSecret = ''
    userAgent = ''
    username = ''
    password = ''
    
    for line in data:
        if line.startswith("#"):
            continue
        
        key = line.split("=")[0]
        value = line.split('=')[1]
        
        if key == 'client_id':
            cId = value
            continue
        if key == 'client_secret':
            cSecret = value
            continue
        if key == 'user_agent': 
            userAgent = value
            continue
        if key == 'username':
            username = value
            continue
        if key == 'password':
            password = value
            continue
        
        print("Unrecognized key: " + key)
        
    return RedditManager(cId, cSecret, userAgent, username, password)
    

def parseEvents(eventList):
    postText = "\n"
    hasApplied = False
    
    for event in sorted(eventList):
        hasApplied = False
        for e in eventList.get(event):
            if not hasApplied:
                postText += "\n## "
                postText += str(e.get_start())[0:10]
                postText += "\n"
                hasApplied = True
            postText += "\n\n### " + e.get_summary()
            postText += "\n\n###  DESCRIPTION: \n" + e.get_description()
            
            # Parse time
            hour = 0
            minutes = "0"
            try:
                hour = int(str(e.get_start())[11:13])
                minutes = str(e.get_start())[14:16]
            except:
                pass

            timeStr = ''
            
            if hour > 12:
                hour -= 12
                timeStr = str(hour) + ":" + minutes + " PM"
            elif hour == 12:
                timeStr = "12:" + minutes + " PM"
            else:
                timeStr = str(hour) + ":" + minutes + " AM"
                
            postText += "\n\n###  TIME: " + timeStr
            postText += "\n\n###  ADDRESS: " + e.get_address()
            postText += "\n### -- END OF EVENT --"
        postText += "\n"
    return postText
            

def computeEvents(eventList):
    calendar = dict()
    
    for event in eventList:
        dateStr = str(event.get_start())
        
        # Find year / month / day
        year = dateStr[0:4]
        month = dateStr[5:7]
        day = int(dateStr[8:10])
        
        # Throw out events not within a week of the future 
        if day - CalendarManager.getDay() > 0 and day - CalendarManager.getDay() <= 7:
            pass
        else:
            continue
        
        # Make sure it is part of this year & month
        if not CalendarManager.getYear() == year:
            continue
        
        if not CalendarManager.getMonth() == month:
            continue
        
        try:
            # Oh noes
            arr = calendar[day]
            arr.append(event)
            print("Multiple events in one day!")
        except KeyError:
            arr = list()
            
            arr.append(event)
            calendar[day] = arr

        
        
        print("year: " + year)
        print("month: " + month)
        # print("day: " + day)
        
        print("date: " + dateStr)
        print("today:" + CalendarManager.getDateString())
    
    return calendar    
    
    
__init__()
