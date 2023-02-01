from flask import Flask
from flask_sqlalchemy import SQLAlchemy


PROJECT_FOLDER = "cloud_server"

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from cloud_server import routes

