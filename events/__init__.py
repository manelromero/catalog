from flask import Flask
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Event, Base

app = Flask(__name__)
# config file for development
app.config.from_object('config')

# config file por production
app.instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), \
	'..'))
config_file_path = app.instance_path + '/instance/config.py'
app.config.from_pyfile(config_file_path)

# database connection
engine = create_engine('sqlite:///tickets.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

import views