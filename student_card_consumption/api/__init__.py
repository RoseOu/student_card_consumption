# coding: utf-8
'''
    api
    ``````````
    : The API module of student_card_consumpotion backend
    ............

    : copyright: (c) 2017 by MuxiStudio
    : license: MIT
'''
from flask import Blueprint

api = Blueprint('api', __name__)

from . import getConsume,errors
