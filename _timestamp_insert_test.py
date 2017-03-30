# coding: utf-8
# python -i filename to open
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:////' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
moment = Moment(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime)
    
 #   def __init__(self, timestamp):
 #       self.timestamp = timestamp

    def __repr__(self):
        return '<User %r>' % self.id

db.create_all()                          #创建表 
u = Users(timestamp=datetime.utcnow())
db.session.add(u)
db.session.commit()

peter = Users.query.filter_by(id=1).first()
print peter.timestamp