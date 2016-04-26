#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from taskListReader import taskListReader
from icalendar import Calendar, Event
from datetime import date, timedelta
import sys

def taskToCal( filename):
    cal = Calendar()

    cal.add('prodid', '-//moozer/zimToCal//')
    cal.add('version', '2.0')

    reader = taskListReader( filename )
    while True:
        try:
            t = reader.next()
      
            event = Event()
            event.add('summary', t["description"])
            event.add('dtstart', t["date"] )
            event.add('dtend', t["date"]+timedelta(days=1) )
            
            cal.add_component(event)
        except ValueError, ex:
            print >> sys.stderr, "ValueError reported: %s"%ex
            continue
        except StopIteration:
            break
            
    # and output to stdout
    print cal.to_ical()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: "
        print "  %s <path to index.db>"%sys.argv[0]
        exit()
        
    taskToCal( sys.argv[1] )
