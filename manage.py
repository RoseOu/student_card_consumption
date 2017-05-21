# coding: utf-8
"""
    manage.py

"""
import os
import sys
import importlib
from flask_script import Manager, Shell
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from student_card_consumption import db, app
from student_card_consumption.models import Student,Deal
from datetime import datetime

importlib.reload(sys)

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        Student = Student,
        Deal = Deal
    )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    pass

if __name__ == "__main__":
    manager.run()
