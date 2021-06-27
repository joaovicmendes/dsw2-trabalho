from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'as61d6as5da6ssd8s3a3a858d1as23d1a6s'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)

from flaskblog import api_hoteis, api_promos, api_sites, api_user, routes