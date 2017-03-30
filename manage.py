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
from flask_migrate import migrate, MigrateCommand    #什么是MigrateCommand
from student_card_consumption import db, app
from student_card_consumption.models import Student_card_consumption_table1, Student_card_consumption_table2
from datetime import datetime


#set encoding to utf-8
#but reload is monster:(
reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate(app, db)

#开始的时候用Student_card_consumption_table1
current_table = Student_card_consumption_table1

reference_timestamp = datetime(2017, 1, 1)
def switch_database_table(table1, table2, current_table):
    #current_timestamp = datetime.utcnow() + timedelta(hours=8)
    #diff = current_timestamp - reference_timestamp
    #diff_days = diff.days
    #if diff % 3:
    if current_table == table1:
        current_table.query.delete()
        current_table = table2
        current_table.insert_all_consumption_data()
    else:
        current_table.query.delete()
        current_table = table1
        current_table.insert_all_consumption_data()
    db.session.commit()
    return current_table 

#????不知道放在哪里
current_timestamp = datetime.utcnow() + timedelta(hours=8)
diff = current_timestamp = reference_timestamp
diff_days = diff.days
if (diff_days // 2) % 2 == 0:   #每4天切换一次数据库
    switch_database_table(Student_card_consumption_table1, Student_card_consumption_table2, current_table)

def make_shell_context():
    shell_ctx = dict(app = app, db = db, Student_card_consumption=Student_card_consumption)
    return shell_ctx
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command 
def test(coverage=False):
    #测试用，以后来写
    pass

#没1或3天更新一次student_card_consumption_table数据库表
@manager.command
def update_STDCC_db(arg):
    from datetime import datetime
    CurrentLocalTime = datetime.utcnow()
    Student_card_consumption_table1.insert_all_consumption_data()
    


if __name__ == "__main__":
    if sys.argv[1] == 'test' or sys.argv[1] == 'lint':
        os.environ['STDCC_CONFIG'] = 'test'
    manager.run()
    #????不知道放在哪里
    current_timestamp = datetime.utcnow() + timedelta(hours=8)
    diff = current_timestamp = reference_timestamp
    diff_days = diff.days
    if (diff_days // 2) % 2 == 0:   #每4天切换一次数据库
        switch_database_table(Student_card_consumption_table1, Student_card_consumption_table2, current_table)