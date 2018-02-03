# coding: utf-8
"""
    manage.py

"""
import os
import sys
from flask_script import Manager, Shell
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from student_card_consumption import db, app
from student_card_consumption.models import Student,Deal
from student_card_consumption.crawler import calculate,create
from datetime import datetime

reload(sys)

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
def add2014():
    #student2014=range(2014210001, 2014214841)
    student2014=range(2014213420, 2014214841)
    studentlist = [student2014]
    #create.create_students(studentlist)
    print "-- create_student done! --"
    create.create_deals(studentlist)
    print "-- create_deals done! --"

@manager.command
def add2015():
    student2015=range(2015210001, 2015214595)
    studentlist = [student2015]
    #create.create_students(studentlist)
    print "-- create_student done! --"
    create.create_deals(studentlist)
    print "-- create_deals done! --"

@manager.command
def add2016():
    #student2016=range(2016210001, 2016214643)
    student2016=range(2016210870, 2016210871)
    studentlist = [student2016]
    #create.create_students(studentlist)
    print "-- create_student done! --"
    create.create_deals(studentlist)
    print "-- create_deals done! --"

@manager.command
def add2017():
    student2017=range(2017210001, 2017214917)
    studentlist = [student2017]
    #create.create_students(studentlist)
    print "-- create_student done! --"
    create.create_deals(studentlist)
    print "-- create_deals done! --"

@manager.command
def calculate_all_students():
    calculate.calculate_all()
    print "-- calculate done! --"


if __name__ == "__main__":
    manager.run()
