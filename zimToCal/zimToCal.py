#!/usr/bin/env python

# outputs the tasks from the iterator as ical to stdout
#
# adapted from here:
#  http://icalendar.readthedocs.org/en/latest/usage.html

from zimToCal.TaskListReader import TaskListReader
from icalendar import Calendar, Event
from datetime import timedelta, datetime
import sys
from collections import namedtuple

import argparse


def addCalHeaders(cal):
    cal.add('prodid', '-//moozer/zimToCal//')
    cal.add('version', '2.0')


def addCalEvent(cal, task):
    event = Event()
    event.add('summary', task.description)

    if task.time:  # if time is included - it takes 1 h
        initialTime = datetime.combine(task.date, datetime.min.time())
        startTime = initialTime + timedelta(hours=task.time[0], minutes=task.time[1])
        endTime = startTime + timedelta(hours=1)
    else:  # it is an all-day event
        startTime = task.date
        endTime = startTime + timedelta(days=1)

    event.add('dtstart', startTime)
    event.add('dtend', endTime)

    cal.add_component(event)


def task_to_cal(config):
    cal = Calendar()
    addCalHeaders(cal)

    reader = TaskListReader(config)
    while True:
        try:
            task = reader.next()
            addCalEvent(cal, task)
        except ValueError as ex:
            print >> sys.stderr, "ValueError reported: %s" % ex
            continue
        except StopIteration:
            break

    return cal.to_ical()


def setup_arg_parse():
    parser = argparse.ArgumentParser(description='Output zim tasks')
    parser.add_argument("filename",
                        help="the index.db file to use")
    parser.add_argument('-t', '--limit-tags',
                        help='Include only tasks with this tag',
                        required=False)
    parser.add_argument('-c', '--closed-tasks',
                        help='Show closed tasks (default: do not show closed tasks )',
                        required=False, action='store_true',
                        default=False)
    parser.add_argument('-no', '--not-open-tasks', help='Show open tasks (default: show open tasks )',
                        required=False, action='store_true',
                        default=False)

    return parser.parse_args()


ConfigStruct = namedtuple('ConfigStruct', ['filename', 'limit_tags', 'closed_tasks', 'not_open_tasks'])

if __name__ == "__main__":
    config = setup_arg_parse()
    print (task_to_cal(config))
