# coding: utf-8
"""
    manage.py

    :[intro]
    :--student_card_consumption backend management

    :[shell]
     -- python manage.py db init    由flask_migrate,与flask_script提供
     -- python manage.py db upgrade 由flask_migrate,与flask_script提供
     -- python manage.py db migrate 由flask_migrate,与flask_script提供
     -- python manage.py db --help  由flask_migrate,与flask_script提供
     #-- python manage.py update_db  更新数据库
     -- python manage.py runserver
     #-- python manage.py test
     #-- python manage.py clear_a_table   清理单个的表(会有位置参数)
     #-- python manage.py clear_all_table 清理所有的表
     -- python manage.py delete_data_from -t (--table=)
"""
import os
#This place is used for test code

import sys

from flask_script import Manager, Shell, Command, prompt_bool
from flask import Flask
from flask_migrate import Migrate, MigrateCommand    #什么是MigrateCommand
from student_card_consumption import db, app
from student_card_consumption.models import Student_card_consumption_table, Page2_data, Page3_data, Page4_data, Page5_data
from datetime import datetime


#set encoding to utf-8
#but reload is evil:(
reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server())
shell = Shell(use_ipython = true)

def make_shell_context():
    shell_ctx = dict(app = app, db = db, Student_card_consumption_table=Student_card_consumption_table, Page2_data=Page2_data,
    Page3_data=Page3_data, Page4_data=Page4_data, Page5_data=Page5_data)
    return shell_ctx
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command 
def test(coverage=False):
    #测试用，以后来写
    pass

@manager.command
def insert_all_student_consumption_data():
    db.create_all()
    Student_card_consumption_table.insert_all_consumption_data()


#One command reload all data
@manager.command
def insert_all_Page_data():
    Page2_data.insert_all_Page2_data()
    Page3_data.insert_all_Page3_data()
    Page4_data.insert_all_Page4_data()
    Page5_data.insert_all_page5_data()
    Page5_data.insertAllRanking()

#新添加的命令，未测试
@manager.command
def add_new_consumption_data():
    data = dict()
    userId_str = raw_input("student_id>")
    data['orgName'] = raw_input("orgName>")
    data['dealDateTime'] = raw_input("dealDateTime(format:%Y-%m-%d HH:MM:HH)>")
    data['transMoney'] = float(raw_input('transMoney'))
    Student_card_consumption_table.insert_consumption_data(data, int(userId))


@manager.command
def Hello():
    '''just say hello'''
    print "hello"

@manager.option('-t', '--table', dest='table', default='STDCC_table',help='the table to be clear')
def delete_data_from(table):
    if 
    print 'Aha!', table

@manager.command
def dropdb():
    '''drop all data'''
    if prompt_bool("Are you sure you want to lose all data"):
        db.drop_all()
    
if __name__ == "__main__":
    if sys.argv[1] == 'test' or sys.argv[1] == 'lint':
        os.environ['STDCC_CONFIG'] = 'test'
    manager.run()