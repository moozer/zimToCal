# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

# -- Extra stuff to handle timedate nummbers in sqlite --------
from sqlalchemy import types
from sqlalchemy import event, Table


class MyEpochType(types.TypeDecorator):
    impl = types.Integer

    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)

    def process_bind_param(self, value, dialect):
        return (value / 1000 - self.epoch).total_seconds()

    def process_result_value(self, value, dialect):
        return self.epoch + datetime.timedelta(seconds=value / 1000)


@event.listens_for(Table, "column_reflect")
def setup_epoch(inspector, table, column_info):
    if isinstance(column_info['type'], types.DateTime):
        column_info['type'] = MyEpochType()


# ----------

Base = declarative_base()
metadata = Base.metadata


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    parent = Column(ForeignKey(u'files.id'))
    path = Column(Text, nullable=False, unique=True)
    node_type = Column(Integer, nullable=False)
    mtime = Column(DateTime)
    index_status = Column(Integer, server_default=text("3"))

    parent1 = relationship(u'File', remote_side=[id])


t_links = Table(
    'links', metadata,
    Column('source', ForeignKey(u'pages.id')),
    Column('target', ForeignKey(u'pages.id')),
    Column('rel', Integer),
    Column('names', Text),
    Column('anchorkey', Text),
    Column('needscheck', Boolean, server_default=text("0")),
    UniqueConstraint('source', 'rel', 'names')
)


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    parent = Column(ForeignKey(u'pages.id'))
    n_children = Column(Integer, server_default=text("0"))
    name = Column(Text, nullable=False, unique=True)
    sortkey = Column(Text, nullable=False)
    mtime = Column(MyEpochType)
    source_file = Column(ForeignKey(u'files.id'))
    is_link_placeholder = Column(Boolean, server_default=text("0"))

    parent1 = relationship(u'Page', remote_side=[id])
    file = relationship(u'File')
    tags = relationship(u'Tag', secondary='tagsources')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    sortkey = Column(Text)


t_tagsources = Table(
    'tagsources', metadata,
    Column('source', ForeignKey(u'pages.id')),
    Column('tag', ForeignKey(u'tags.id')),
    UniqueConstraint('source', 'tag')
)


class Tasklist(Base):
    __tablename__ = 'tasklist'

    id = Column(Integer, primary_key=True)
    source = Column(Integer)
    parent = Column(Integer)
    haschildren = Column(Boolean)
    hasopenchildren = Column(Boolean)
    open = Column(Boolean)
    prio = Column(Integer)
    start = Column(Text)
    due = Column(Text)
    tags = Column(Text)
    description = Column(Text)


t_zim_index = Table(
    'zim_index', metadata,
    Column('key', Text, unique=True),
    Column('value', Text)
)
