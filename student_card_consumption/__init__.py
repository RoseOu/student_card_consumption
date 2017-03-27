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

from flask_sqlalchemy import SQLAlchemy 
from flask_moment import Moment 


#Flask extention
db = SQLAlchemy()
moment = Moment()

