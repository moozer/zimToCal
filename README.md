zimToCal
=========

This is a simple script intended to be run as a cron job.

It takes the supplied zim index file, and converts the task list to a calendar file.


python requirements
--------------------

It require the icalendar package

    apt-get install python-icalendar

or use pip or whatever other python specific handler you prefer.


usage
------

To just generate the .ics file

    zimToCal <path to cache file> > zimTasks.ics
    
The cache file probably resides in ~/.cache/zim


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
