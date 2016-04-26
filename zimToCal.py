#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from taskListReader import taskListReader
from icalendar import Calendar, Event
from datetime import date, timedelta
import sys

def addCalHeaders( cal ):
    cal.add('prodid', '-//moozer/zimToCal//')
    cal.add('version', '2.0')

def addCalEvent( cal, task ):
    event = Event()
    event.add('summary', task["description"])
    event.add('dtstart', task["date"] )
    event.add('dtend', task["date"]+timedelta(days=1) )    
    cal.add_component(event)

def taskToCal( filename):
    cal = Calendar()
    addCalHeaders( cal )

    reader = taskListReader( filename )
    while True:
        try:
            task = reader.next()
            addCalEvent( cal, task )            
        except ValueError, ex:
            print >> sys.stderr, "ValueError reported: %s"%ex
            continue
        except StopIteration:
            break
            
    # and output to stdout
    return cal.to_ical()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: "
        print "  %s <path to index.db>"%sys.argv[0]
        exit()
        
    print taskToCal( sys.argv[1] )
