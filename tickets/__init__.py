from flask import Flask
import os

app = Flask(__name__)
# config file for development
app.config.from_object('config')

# config file por production
app.instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), \
	'..'))
config_file_path = app.instance_path + '/instance/config.py'
app.config.from_pyfile(config_file_path)

import views