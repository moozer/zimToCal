import unittest
from zimToCal import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytz

db_filename = '../testData/index.db'
test_config = ConfigStruct(filename=db_filename,
                           not_open_tasks=False,
                           closed_tasks=False,
                           limit_tags=None)

task_id_1 = task_record(date=datetime.date(2016, 1, 1), description=u'Task A', time=None, open=True,
                        tags=u'', path=[u'Home'], priority=0, reach=None, parent_id=0,
                        id=1, datetime=datetime.datetime(2016, 1, 1, 0, 0, tzinfo=pytz.timezone('Europe/Copenhagen')))

task_id_2 = task_record(date=datetime.date(2016, 1, 2), description=u'Task B', time=None, open=True,
                        tags=u'', path=[u'Home'], priority=0, reach=None, parent_id=0,
                        id=2, datetime=datetime.datetime(2016, 1, 2, 0, 0, tzinfo=pytz.timezone('Europe/Copenhagen')))


class TestDbAccess(unittest.TestCase):
    def setUp(self):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))

        db_string = 'sqlite:///{}/{}'.format(dir_path, test_config.filename)

        sqlite_engine = create_engine(db_string)
        Session = sessionmaker(bind=sqlite_engine)
        self.session = Session()

    def test_page_query(self):
        parent_page = self.session.query(Page).filter(zim_db.Page.id == 2).one()
        self._baseAssertEqual(parent_page.id, 2)


class TestTaskListReader(unittest.TestCase):
    def setUp(self):
        self.tl = TaskListReader(test_config)

    def test_get_task(self):
        task = self.tl.get_task_by_id(2)
        self.assertEqual(task, task_id_2)

    def test_get_task_parent(self):
        p_id = self.tl.get_parent_task_id(2)
        self.assertEqual(p_id, task_id_2.parent_id)

    def test_get_task_parent(self):
        p_id = self.tl.get_parent_task_id(2)
        self.assertEqual(p_id, task_id_2.parent_id)

    def test_get_tasks(self):
        tasks = self.tl.get_tasks_generator()
        for t in tasks:
            self.assertEqual(t, task_id_1)
            break

