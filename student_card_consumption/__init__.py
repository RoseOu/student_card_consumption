# coding: utf-8
'''
    __init__.py
    `````````````
    : Flask extention init
    : Flask app create
    : Flask blueprint register
    ................
    
    : copyright: (c) 2017 by MuxiStudio

'''
import os

from flask_sqlalchemy import SQLAlchemy 
from flask_moment import Moment 
from STDCC_config import config
from flask import Flask


#Flask extention
db = SQLAlchemy()
moment = Moment()

from . import models

def create_app(config_name = None, main = True):
    """
        student_card_consumption app factory function 

        param config_name : current configrued enviroment //当前配置环境
        param main : main process moudels name //主进程名称
    """
    if config_name is None:
        config_name = os.environ.get("STDCC_SETTING", "default")    #config STDCC_SETTING as environment variable
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #initial flask extention
    db.init_app(app)
    moment.init_app(app)

    #blueprint
    from api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app

#student_card_consumption app
app = create_app(config_name = os.getenv('STDCC_config') or 'default')