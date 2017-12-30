import sqlite3
import re
from datetime import datetime, date
from collections import namedtuple
import pytz


def extractTime(taskText):
    """ extracts the hours like " 10:03 " from start of the text
    """
    timeRegex = '^\ {0,1}\d{1,2}:\d{2}\ {0,}'
    parser = re.compile(timeRegex)

    timeTextFind = parser.match(taskText)
    if timeTextFind:
        timeText = [int(x) for x in timeTextFind.group().strip().split(':')]
    else:
        timeText = None

    newText = parser.sub('', taskText)
    return (timeText, newText)


def removeTag(taskText, tag):
    """ extracts the hours like " 10:03 " from start of the text
    """
    timeRegex = "@%s" % (tag,)
    parser = re.compile(timeRegex)
    newText = parser.sub('', taskText)
    return newText


def extractReach(taskText):
    """ extracts the hours like " r08 " from the start of text
    """
    reachRegex = '^\ {0,1}r{1}\d{1,3}\ {0,}'
    parser = re.compile(reachRegex)

    reachTextFind = parser.match(taskText)
    if reachTextFind:
        reach_days = int(reachTextFind.group().strip()[1:])
    else:
        reach_days = None

    newText = parser.sub('', taskText)
    return (reach_days, newText)


task_record = namedtuple('task_record',
                         ["date", "description", "time",
                          "open", "tags", "path",
                          "priority", "reach", "parent_id",
                          "id", "datetime"])


class TaskListReader(object):
    """ reads the tasklist cache file and outputs

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

    """

    def __init__(self, config):
        self.dbfilename = config.filename
        self.config = config
        self.con = sqlite3.connect(self.dbfilename)

        self.tasks_query_cur = self._query_tasks()

        try:
            self.default_tz = pytz.timezone(config.default_time_zone_name)
        except AttributeError:
            self.default_tz = pytz.timezone('Europe/Copenhagen')

    def __iter__(self):
        return self

    def next(self):
        row = self.tasks_query_cur.fetchone()
        if not row:
            raise StopIteration

        next_task = self._create_task_from_row(row)
        return next_task

    def _create_task_from_row(self, row):
        try:
            due, description, open_status, tags, source_id, prio, parent_id, task_id = row
            path = self._get_parent_pages(source_id)
            result = re.sub('\[.*\]', '', description)

            y, m, d = [int(i) for i in due.split('-')]
            timeText, newText = extractTime(result)
            reach_days, newText = extractReach(newText)
            newText = removeTag(newText, self.config.limit_tags)

            task = task_record(
                date=date(y, m, d),
                datetime=datetime(y, m, d, tzinfo=self.default_tz),
                description=newText,
                time=timeText, open=open_status,
                tags=tags, path=path, priority=prio,
                reach=reach_days,
                parent_id=parent_id, id=task_id)

            return task

        except ValueError:
            raise ValueError("Possible date error in task '%s'" % description)

    def _query_tasks(self):
        cur = self.con.cursor()

        # 9999 is the magic number for "no due date"
        query = 'select due, description, open, tags, source, prio, parent, id from tasklist where due != "9999"'

        if not self.config.closed_tasks and not self.config.not_open_tasks:
            query += " and open = 1"
        elif self.config.closed_tasks and self.config.not_open_tasks:
            query += " and open = 0"
        # else: nothing

        if not self.config.limit_tags:
            cur.execute(query)
        else:
            cur.execute(query + ' and tags=?', (self.config.limit_tags,))

        return cur

    def _get_parent_pages(self, pageid):
        parent_id, basename = self._get_parent_page(pageid)

        if parent_id == 0:
            return []

        prevpages = self._get_parent_pages(parent_id)
        prevpages.append(basename)
        return prevpages

    def _get_parent_page(self, pageid):
        cur = self.con.cursor()
        query = "select parent, name from pages where id = ?"
        cur.execute(query, (pageid,))
        return cur.fetchone()

    def _get_parent_task(self, task_id):
        cur = self.con.cursor()

        # 9999 is the magic number for "no due date"
        query = 'select t.id, p.id, p.description \
                 from tasklist t \
                 inner join tasklist p \
                 on p.id = t.parent \
                 where t.id = ?'

        cur.execute(query, (task_id,))
        return cur.fetchone()

    def get_task(self, task_id):
        cur = self.con.cursor()
        query = 'select due, description, open, tags, source, prio, parent, id from tasklist where parent=?'
        cur.execute(query, (task_id,))
        return self._create_task_from_row(cur.fetchone())
