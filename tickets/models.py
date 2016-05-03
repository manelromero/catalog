from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user = Column(String(8), primary_key=True)
    password = Column(String(8))

    @property
    def login_user(self):
        print self


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event = Column(String(80))
    description = Column(String(200))
    date = Column(Date)
    location = Column(String(80))
