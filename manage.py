# coding: utf-8
"""
    manage.py

    :[intro]
    :--student_card_consumption backend management

    :[shell]
     -- python manage.py db init    由flask_migrate提供
     -- python manage.py db upgrade 由flask_migrate提供
     -- python manage.py db migrate 由flask_migrate提供
     -- python manage.py db update  更新数据库
     -- python manage.py db --help
     -- python manage.py runserver
     -- python manage.py test
"""
import os
#This place is used for test code

import sys
import base64

from flask_script import Manager, Shell
from flask import Flask
from flask_migrate import migrate, MigrateCommand    #什么是MigrateCommand
from student_card_consumption import db, app
from student_card_consumption.models import student_card_consumption

#set encoding to utf-8
#but reload is monster:(
reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    shell_ctx = dict(app = app, db = db, Student_card_consumption=Student_card_consumption)
    return shell_ctx
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command 
def test(coverage=False):
    #测试用，以后来写
    pass

@manager.command
def 