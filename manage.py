# coding: utf-8
"""
    manage.py

    :[intro]
    :--student_card_consumption backend management

    :[shell]
     -- python manage.py db init
     -- python manage.py db upgrade
     -- python manage.py db migrate
     -- python manage.py runserver
"""

import sys
import base64

from flask_script import Manager, Shell
from flask import Flask
from flask_migrate import migrate
from student_card_consumption import db, app
from student_card_consumption.models import student_card_consumption

#set encoding to utf-8
#but reload is monster:(
reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    shell_ctx = dict(app = app, db = db, )
    return shell_ctx
    