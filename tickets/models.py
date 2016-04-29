from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
	__tablename__ = 'categories'
	# Columns
	id = Column(Integer, primary_key=True)
	name = Column(String(80))

class Event(Base):
	__tablename__ = 'events'
	#Columns
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	description = Column(String(200))
	date = Column(Date)
	location = Column(String(80))
