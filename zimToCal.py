#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from taskListReader import taskListReader
from icalendar import Calendar, Event

cal = Calendar()
from datetime import date, timedelta

cal.add('prodid', '-//moozer/zimToCal//')
cal.add('version', '2.0')

for t in taskListReader( "testData/index.db" ):
    
    event = Event()
    event.add('summary', t["description"])
    event.add('dtstart', t["date"] )
    event.add('dtend', t["date"]+timedelta(days=1) )
    
    cal.add_component(event)

# and output to stdout
print cal.to_ical()
