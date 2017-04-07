

import sqlite3
import re
from datetime import date
from collections import namedtuple

def extractTime( taskText ):
    ''' extracts the hours like " 10:03 " from the text
    '''
    timeRegex = '^\ {0,1}\d{1,2}:\d{2}\ {0,}'
    parser = re.compile( timeRegex )

    timeTextFind = parser.match( taskText )
    if timeTextFind:
        timeText = [int(x) for x in timeTextFind.group().strip().split(':')]
    else:
        timeText = None

    newText = parser.sub( '', taskText)
    return (timeText, newText)

task_record = namedtuple('task_record', ["date", "description", "time", "open", "tags"])


class taskListReader( object ):
    ''' reads the tasklist cache file and outputs

    and becomes an iterable object

    From the database

    sqlite> .schema tasklist
    CREATE TABLE tasklist (
        id INTEGER PRIMARY KEY,
        source INTEGER,
        parent INTEGER,
        haschildren BOOLEAN,
        open BOOLEAN,
        actionable BOOLEAN,
        prio INTEGER,
        due TEXT,
        tags TEXT,
        description TEXT
    );

    '''
    def __init__( self, config ):
        self.dbfilename = config.filename

        self.con = sqlite3.connect( self.dbfilename )
        self.cur = self.con.cursor()

        # 9999 is the magic number for "no due date"
        query = 'select due, description, open, tags, source from tasklist where due != "9999"'

        if config.closed_tasks:
            query += " and open = 0"
        else:
            query += " and open = 1"

        if not config.limit_tags:
            self.cur.execute( query )
        else:
            self.cur.execute( query + ' and tags=?', (config.limit_tags, ) )

    def __iter__( self ):
        return self

    def next( self ):
        try:
            due, description, open_status, tags, source_id = self.cur.fetchone()

            print source_id
            print self._get_parent_page( source_id )

            result = re.sub('\[.*\]', '', description)
            y,m,d = [int(i) for i in due.split('-')]
            timeText, newText = extractTime( result )
            nexttask = task_record(
                        date=date( y,m,d ), description=newText,
                        time=timeText, open=open_status,
                        tags=tags )

            return nexttask

        except ValueError:
            raise ValueError( "Possible date error in task '%s'"%description)

        except TypeError:
            raise StopIteration

    def _get_parent_page( self, pageid ):
        print "pageid", pageid

        cur = self.con.cursor()

        query = "select parent, basename from pages where id = ?"
        cur.execute( query, (pageid, ) )

        parent_id, pagename = cur.fetchone()
        return parent_id, pagename

# a simple test to show syntax
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

if __name__ == "__main__":
    config = { "filename": "testData/index.db",
                "closed_tasks": False,
                "limit_tags": None}

    tasks = taskListReader( AttrDict( config ) )
    for t in tasks:
        print t
