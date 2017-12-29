import unittest

from zimToCal import *

test_config = ConfigStruct( filename='../testData/index.db',
                            not_open_tasks=False,
                            closed_tasks=False,
                            limit_tags=None)

class MyTestCase(unittest.TestCase):

    def test_setup_arg_parse(self):
        with self.assertRaises(SystemExit):
            # fails due to to missing mandatory command line parameter.
            setup_arg_parse()

    def test_task_to_stdout(self):
        task_to_stdout( test_config )

    def test_task_to_cal(self):
        print task_to_cal( test_config )


if __name__ == '__main__':
    unittest.main()
