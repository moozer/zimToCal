#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from taskListReader import taskListReader, extractTime
import argparse

def setupArgparse():
    parser = argparse.ArgumentParser(description='zimToCal convert zim tasks to ics.')
    parser.add_argument("filename", help="the index.db file to use" )
    parser.add_argument('-t','--limit-tags',   help='Include only tasks with this tag', required=False)
    parser.add_argument('-c','--closed-tasks', help='Show only closed tasks (default: show only open tasks)',
                                               required=False, action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    config = setupArgparse()

    for t in taskListReader( config ):
        if not t.time:
            output = "%s\t\t%s\t%s\t%s"%(t.date, t.open, t.tags, t.description)
        else:
            output = "%s\t%d:%02d\t%s\t%s\t%s"%(t.date, t.time[0], t.time[1], t.open, t.tags, t.description)

        print output.encode('utf-8')
