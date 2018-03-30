import unittest
from zimToCal import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_config = ConfigStruct(filename='/home/moz/git/zimToCal/testData/index.db',
                           not_open_tasks=False,
                           closed_tasks=False,
                           limit_tags=None)


class testDbAccess(unittest.TestCase):
    def setUp(self):
        db_string = 'sqlite:///{}'.format(test_config.filename)
        print db_string

        sqlite_engine = create_engine(db_string)
        Session = sessionmaker(bind=sqlite_engine)
        self.session = Session()

    def test_page_query(self):
        parent_page = self.session.query(Page).filter(zim_db.Page.id == 2).one()
        self._baseAssertEqual(parent_page.id, 2)

# class TestTaskListReader(unittest.TestCase):
#
#    def test_init(self):
#        zimToCal
#        self.assertEqual(test_config.filename, '../testData/index.db')
