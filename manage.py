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
     -- python manage.py update_db  更新数据库
     -- python manage.py runserver
     -- python manage.py test
"""
import os
#This place is used for test code

import sys
import base64

from flask_script import Manager, Shell
from flask import Flask
from flask_migrate import Migrate, MigrateCommand    #什么是MigrateCommand
from student_card_consumption import db, app
from student_card_consumption.models import Student_card_consumption_table, Page2_data, Page3_data, Page4_data, Page5_data
from datetime import datetime


#set encoding to utf-8
#but reload is monster:(
reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate(app, db)



#reference_timestamp = datetime(2017, 1, 1)
#def switch_database_table(table1, table2, Student_card_consumption):
#    current_timestamp = datetime.utcnow() + timedelta(hours=8)
#    diff = current_timestamp - reference_timestamp
#    diff_days = diff.days
#    if diff % 3:
#    if Student_card_consumption == table1:
#        Student_card_consumption.query.delete()
#        Student_card_consumption = table2
#        Student_card_consumption.insert_all_consumption_data()
#    else:
#        Student_card_consumption.query.delete()
#        Student_card_consumption = table1
#        Student_card_consumption.insert_all_consumption_data()
#    db.session.commit()
#    return Student_card_consumption 



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
    
@manager.command
def Hello():
    print "hello"

if __name__ == "__main__":
    if sys.argv[1] == 'test' or sys.argv[1] == 'lint':
        os.environ['STDCC_CONFIG'] = 'test'
    manager.run()