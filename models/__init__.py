from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()
engine = create_engine('mysql+pymysql://root:admin@localhost/test?charset=utf8')

