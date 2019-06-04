import sqlalchemy

import zimToCal.zim_db
import re
from datetime import datetime, date
from collections import namedtuple
import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def extract_time(task_text):
    """ extracts the hours like " 10:03 " from start of the text
    """
    time_regex = '^\ {0,1}\d{1,2}:\d{2}\ {0,}'
    parser = re.compile(time_regex)

    time_text_find = parser.match(task_text)
    if time_text_find:
        time_text = [int(x) for x in time_text_find.group().strip().split(':')]
    else:
        time_text = None

    new_text = parser.sub('', task_text)
    return time_text, new_text


def remove_tag(task_text, tag):
    """ extracts the hours like " 10:03 " from start of the text
    """
    time_regex = "@%s" % (tag,)
    parser = re.compile(time_regex)
    new_text = parser.sub('', task_text)
    return new_text


def extract_reach(task_text):
    """ extracts the hours like " r08 " from the start of text
    """
    reach_regex = '^\ {0,1}r{1}\d{1,3}\ {0,}'
    parser = re.compile(reach_regex)

    reach_text_find = parser.match(task_text)
    if reach_text_find:
        reach_days = int(reach_text_find.group().strip()[1:])
    else:
        reach_days = None

    new_text = parser.sub('', task_text)
    return reach_days, new_text


task_record = namedtuple('task_record',
                         ["date", "description", "time",
                          "open", "tags", "path",
                          "priority", "reach", "parent_id",
                          "id", "datetime"])


class TaskListReader(object):
    """ reads the tasklist cache file and outputs
    """

    def __init__(self, config):
        self.dbfilename = config.filename
        self.config = config

        db_string = 'sqlite:///{}'.format(self.dbfilename)

        sqlite_engine = create_engine(db_string)
        Session = sessionmaker(bind=sqlite_engine)
        self.session = Session()

        try:
            self.default_tz = pytz.timezone(config.default_time_zone_name)
        except AttributeError:
            self.default_tz = pytz.timezone('Europe/Copenhagen')

    def _create_task_from_task_query(self, entry):
        try:
            path = self._get_parent_pages(entry.source)
            result = re.sub('\[.*\]', '', entry.description)

            y, m, d = [int(i) for i in entry.due.split('-')]
            time_text, new_text = extract_time(result)
            reach_days, new_text = extract_reach(new_text)
            new_text = remove_tag(new_text, self.config.limit_tags)

            task = task_record(
                date=date(y, m, d),
                datetime=datetime(y, m, d, tzinfo=self.default_tz),
                description=new_text,
                time=time_text, open=entry.open,
                tags=entry.tags, path=path, priority=entry.prio,
                reach=reach_days,
                parent_id=entry.parent, id=entry.id)

            return task

        except ValueError:
            raise ValueError("Possible date error in task '%s'" % entry.description)

    def get_tasks_generator(self):
        try:
            for t in self._query_tasks():
                yield self._create_task_from_task_query(t)
        except sqlalchemy.orm.exc.NoResultFound:
            raise StopIteration

    def _query_tasks(self):
        # 9999 is the magic number for "no due date"
        tasks_query = self.session.query(zim_db.Tasklist).filter(zim_db.Tasklist.due != '9999')

        if not self.config.closed_tasks and not self.config.not_open_tasks:
            tasks_query = tasks_query.filter(zim_db.Tasklist.open == 1)
        elif self.config.closed_tasks and self.config.not_open_tasks:
            tasks_query = tasks_query.filter(zim_db.Tasklist.open == 0)
        # else: nothing

        if self.config.limit_tags:
            tasks_query = tasks_query.filter(zim_db.Tasklist.tags == self.config.limit_tags)

        return tasks_query

    def _get_parent_pages(self, pageid):
        if pageid == 0:
            return []

        parent_id = self.get_parent_task_id(pageid)
        if parent_id is None:
            return []
        prev_pages = self._get_parent_pages(parent_id)

        # an add this page also
        p_page = self._get_page_by_id(pageid)
        prev_pages.append(p_page.name)

        return prev_pages

    def get_parent_task_id(self, task_id):
        parent_task = self.session.query(zim_db.Tasklist.parent).filter(zim_db.Tasklist.id == task_id).one_or_none()
        if parent_task is None:
            return None
        return parent_task.parent

    def get_task_by_id(self, task_id):
        tasks_query = self.session.query(zim_db.Tasklist).filter(zim_db.Tasklist.id == task_id)
        task = tasks_query.one()
        return self._create_task_from_task_query(task)

    def _get_page_by_id(self, page_id):
        page_query = self.session.query(zim_db.Page).filter(zim_db.Page.id == page_id)
        return page_query.one()
