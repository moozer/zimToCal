#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from taskListReader import taskListReader, extractTime
import argparse
from zimToCal import setupArgparse

if __name__ == "__main__":
    config = setupArgparse()

    for t in taskListReader( config ):
        output = "%s"%(t.date )
        if not t.time:
            output += "\t"
        else:
            output += "\t%d:%02d"%(t.time[0], t.time[1], )
        output += "\t%s\t%s\t%s\t%s"%(t.open, t.priority, t.tags, t.path)
        output += "\t%s"%(t.description, )

        print output.encode('utf-8')
