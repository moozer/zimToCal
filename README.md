zimToCal
=========

This is a simple script intended to be run as a cron job.

It takes the supplied zim index file, and converts the task list to a calendar file.

An example:

```
[] [d:2016-01-01] Task A
[] [d:2016-01-01] 11:30 Task B
```

will end up in the index database, and zimToCal will convert it to 

* Task A (full day event on 2016-01-01)
* Task B (an event at 2016-01-01 at 11:30 with a duration of 1h)

The 1h is hardcoded see [issue #2](https://github.com/moozer/zimToCal/issues/2)

python requirements
--------------------

It require the icalendar package

    apt-get install python-icalendar

or use pip or whatever other python specific handler you prefer.


Basic usage
------

To just generate the .ics file

    zimToCal <path to cache file> <tag> > zimTasks.ics

Paramters:

* path to cache file

  Index file to get data from. The cache file probably resides in ~/.cache/zim

* tag
 
  Limit the calendar entries to task with the specific tag. 

  Notes: This is not pages (see [issue #1](https://github.com/moozer/zimToCal/issues/1)) and this doesn't handle that the tag i one among many.


Hint: use a cron job
----------------------

It will most usefull when it updates itself automatically

Add a line like this in crontab (using *crontab -e*)

    47 * * * * <somepath>/zimToCal.py <path to cache>/index.db > <path to calendar file> <tag> > zimTasks.ics

This will run the script once per hour at 47 minutes past.

I experimented with [incron](http://inotify.aiken.cz/?section=incron&page=doc&lang=en) job, but that was not a good idea, since it ran the script at every update of the db file.


Using the .ics file in thunderbird
--------------------------------------

Do the following:

  - Create a new calendar

  - "on the network"
  
  - "Format: iCalendar (ICS)", and the "location" is file:///home/user/zimToCal/zimTasks.ics
  
  - "Offline support" is not needed
  
  - Give it a name and a color. I suggest setting "E-mail" to none.
  
Clicking properties on the new calendar enables you to set it to read-only.
  
Note that changing the path, once typed is not possible (at least not in my iceweasel).
