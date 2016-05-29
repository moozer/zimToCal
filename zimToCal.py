#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from taskListReader import taskListReader
from icalendar import Calendar, Event
from datetime import date, timedelta, datetime
import re
import sys

def addCalHeaders( cal ):
    cal.add('prodid', '-//moozer/zimToCal//')
    cal.add('version', '2.0')

def addCalEvent( cal, task ):
    event = Event()
    event.add('summary', task["description"])

    if task["time"]: # if time is included - it takes 1 h
        initialTime = datetime.combine(task["date"], datetime.min.time())
        startTime = initialTime + timedelta(hours=task["time"][0], minutes=task["time"][1] )
        endTime = startTime + timedelta( hours=1 )
    else: # it is an all-day event
        startTime = task["date"]
        endTime = startTime+timedelta(days=1)

    event.add('dtstart', startTime )
    event.add('dtend', endTime )    

    cal.add_component(event)

def taskToCal( filename, tag ):
    cal = Calendar()
    addCalHeaders( cal )

    reader = taskListReader( filename, tag )
    while True:
        try:
            task = reader.next()

            timeInfo = extractTime( task["description"] )
            if timeInfo[0]:
                task["description"] = timeInfo[1]
                task["time"] = [int(i) for i in timeInfo[0].split(":")]
            else:
                task["time"] = None
            
            addCalEvent( cal, task )            
        except ValueError, ex:
            print >> sys.stderr, "ValueError reported: %s"%ex
            continue
        except StopIteration:
            break
            
    return cal.to_ical()

def extractTime( taskText ):
    timeRegex = '^\ {0,1}\d{1,2}:\d{2}\ {0,}'
    parser = re.compile( timeRegex )
    
    timeTextFind = parser.match( taskText )
    if timeTextFind:
        timeText = timeTextFind.group().strip()
    else:
        timeText = None
        
    newText = parser.sub( '', taskText)
    return (timeText, newText)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: "
        print "  %s <path to index.db> <tag>"%sys.argv[0]
        exit()
    
    filename = sys.argv[1]
    tag = sys.argv[2] if len(sys.argv) > 2 else None
        
    print taskToCal( filename, tag )
