

import sqlite3
import re
from datetime import date

class taskListReader(  ):
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
    def __init__( self, filename ):
        self.dbfilename = filename
    
        self.con = sqlite3.connect( self.dbfilename )
        self.cur = self.con.cursor()
        
        # 9999 is the magic number for "no due date"
        self.cur.execute('select due, description from tasklist where due != "9999" and open = 1')
 
    def __iter__( self ):
        return self
        
    def next( self ):
        row = self.cur.fetchone()
        if not row:
            raise StopIteration

        result = re.sub('\[.*\]', '', row[1])

        try:
            y,m,d = [int(i) for i in row[0].split('-')]
            nexttask = { "date": date( y,m,d ), 
                        "description": result }
        except ValueError:
            raise ValueError( "Possible date error in task '%s'"%row[1] )
            
        return nexttask        

    
# a simple test to show syntax
if __name__ == "__main__":
    tasks = taskListReader( "testData/index.db" )
    for t in tasks:
        print t
