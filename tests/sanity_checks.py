import unittest
from zimToCal import *
import datetime

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


if __name__ == '__main__':
    unittest.main()
