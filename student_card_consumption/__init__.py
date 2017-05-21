# coding: utf-8
'''
    __init__.py
'''
import os

from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask import Flask


#Flask extention
db = SQLAlchemy()
moment = Moment()

from . import models

def create_app(config_name = None, main = True):
    if config_name is None:
        config_name = 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #initial flask extention
    db.init_app(app)
    moment.init_app(app)

    #blueprint
    from student_card_consumption.api import api
    app.register_blueprint(api, url_prefix='/api')

    return app

app = create_app(config_name = 'default')

