from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from cloud_server import Users
# from cloud_server import AWSCloud 
import cryptocode as crypto
import uuid
import hashlib
from markupsafe import escape


PROJECT_FOLDER = "cloud_server"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///keyforaws.db"
db = SQLAlchemy(app)

from cloud_server import routes

