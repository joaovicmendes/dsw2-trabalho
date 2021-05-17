from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'as61d6as5da6ssd8s3a3a858d1as23d1a6s'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///promos.db'
db = SQLAlchemy(app)

from flaskblog import routes