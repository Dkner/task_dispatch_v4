import time
from sqlalchemy import (
    Column,
    SmallInteger,
    Integer,
    String,
    text
)
from sqlalchemy.orm import sessionmaker
from . import DeclarativeBase, engine


class TaskModel(DeclarativeBase):
    __tablename__ = 'task'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, default='')
    interval_type = Column('interval_type', SmallInteger, default=1)
    time_detail = Column('time_detail', Integer, default=0)
    script = Column('script', String, default='')
    create_at = Column('create_at', Integer, default=0)
    update_at = Column('update_at', Integer, default=0)
    active_host = Column('active_host', String, default='')
    is_bind = Column('is_bind', SmallInteger, default=0)
    exec_status = Column('exec_status', SmallInteger, default=0)
    task_desc = Column('task_desc', String, default='')
    trigger_time = Column('trigger_time', Integer, default=0)

    def __init__(self, task):
        self.name = task.get('name')
        self.interval_type = task.get('interval_type')
        self.time_detail = task.get('time_detail')
        self.script = task.get('script')
        self.create_at = task.get('create_at')
        self.update_at = task.get('update_at')
        self.active_host = task.get('active_host')
        self.is_bind = task.get('is_bind')
        self.exec_status = task.get('exec_status')
        self.task_desc = task.get('task_desc')
        self.trigger_time = task.get('trigger_time')

    @classmethod
    def insert(cls, task):
        new_task = TaskModel(task)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_task)
        session.flush()
        session.commit()

    @classmethod
    def execute(cls, sql):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(text(sql))
        session.commit()

    @classmethod
    def query_task_to_trigger(cls):
        Session = sessionmaker(bind=engine)
        session = Session()
        now = int(time.time())
        session.query(cls).\
            filter(cls.trigger_time < now,
                   cls.exec_status == 0)