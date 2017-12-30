import unittest
from zimToCal import *
import datetime
import pytz

test_config = ConfigStruct(filename='../testData/index.db',
                           not_open_tasks=False,
                           closed_tasks=False,
                           limit_tags=None)

test_task = task_record(date="2017-12-11",
                        description="some description",
                        time="10:00",
                        open=True,
                        tags=['aTag'],
                        path=["first", "second"],
                        priority=4,
                        reach=30,
                        parent_id=10,
                        id=15,
                        datetime=datetime.datetime.strptime("2017-12-11 10:00", "%Y-%m-%d %H:%M"))

first_test_record = task_record(date=datetime.date(2016, 1, 1),
                                description=u'Task A',
                                time=None,
                                open=1,
                                tags=u'',
                                path=[u'Home'],
                                priority=0,
                                reach=None,
                                parent_id=0,
                                id=1,
                                datetime=datetime.datetime(2016, 1, 1, 0, 0, tzinfo=pytz.timezone('Europe/Copenhagen')))

test_C_entry = task_record(date=datetime.date(2016, 1, 3), description=u'Task C', time=None,
                           open=1, tags=u'', path=[u'Home'],
                           priority=0, reach=None, parent_id=0,
                           id=3,
                           datetime=datetime.datetime(2016, 1, 3, 0, 0, tzinfo=pytz.timezone('Europe/Copenhagen')))

test_C1_entry = task_record(date=datetime.date(2016, 1, 3), description=u'Task C1', time=None,
                            open=1, tags=u'', path=[u'Home'],
                            priority=0, reach=None, parent_id=3,
                            id=4,
                            datetime=datetime.datetime(2016, 1, 3, 0, 0, tzinfo=pytz.timezone('Europe/Copenhagen')))


class MyTestCase(unittest.TestCase):

    def test_config_struct(self):
        self.assertEqual(test_config.filename, '../testData/index.db')

    def test_task_record(self):
        self.assertEqual(test_task.time, "10:00")

    def test_setup_arg_parse(self):
        with self.assertRaises(SystemExit):
            # fails due to to missing mandatory command line parameter.
            setup_arg_parse()

    def test_task_to_stdout(self):
        task_to_stdout(test_config)

    def test_task_to_cal(self):
        print task_to_cal(test_config)

    def test_TaskListReader(self):
        tlist = TaskListReader(test_config)

        tr = tlist.next()
        self.assertEqual(tr, first_test_record)

    def test_get_task_by_id(self):
        reader = TaskListReader(test_config)

        task_C = reader.get_task(test_C_entry.id)
        self.assertEqual(task_C, test_C_entry)

        task_C1 = reader.get_task(test_C1_entry.id)
        self.assertEqual(task_C1, test_C1_entry)

if __name__ == '__main__':
    unittest.main()
