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
    student2014=range(2014210001, 2014214841)
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
    student2016=range(2016210001, 2016214643)
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

@manager.command
def calculate_one():
    studentid = 2016210870
    calculate.calculate_test(studentid)
    print "-- calculate done! --"

@manager.command
def calculate2014():
    student2014=range(2014210001, 2014214841)
    calculate.calculate_student_list(student2014)
    print "-- calculate 2014! --"

@manager.command
def calculate2015():
    student2015=range(2015210001, 2015214595)
    calculate.calculate_student_list(student2015)
    print "-- calculate 2015! --"

@manager.command
def calculate2016():
    student2016=range(2016210001, 2016214643)
    calculate.calculate_student_list(student2016)
    print "-- calculate 2016! --"

@manager.command
def calculate2017():
    student2017=range(2017210001, 2017214917)
    calculate.calculate_student_list(student2017)
    print "-- calculate 2017! --"

@manager.command
def delete_student_deal():
    studentlist=range(2014210001, 2014214841)
    for sid in studentlist:
        if Student.query.filter_by(studentid=sid).first():
            student = Student.query.filter_by(studentid=sid).first()
            for d in student.deals:
                db.session.delete(d)
                db.session.commit()
                print "delete" + str(sid)


if __name__ == "__main__":
    manager.run()
