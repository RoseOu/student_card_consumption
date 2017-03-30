#Test pass
from sqlalchemy import Table, Column, String, Integer
from myapplication._database import db_session, metadata
from sqlalchemy.orm import mapper

class User(object):
    query = db_session.query_property()
    def __init__(self, name=None, email=None):
        self.email = email
        self.name = name
    def __repr__(self):
        return '<User %r>' % (self.name)
    
users = Table('users', metadata,             #metadata is from _database.py
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('email', String(120), unique=True)
)
mapper(User, users)

#class User(Base):   
#    __tablename__="user"
#    id = Column(Integer, primary_key=True)
#    name = Column(String(50), unique=True)
#    email = Column(String(200), unique=True)
#    def __init__(self, name=None, email=None):
#        self.name = name
#        self.email = email
#    def __repr__(self):
#        return "<User %r>" % self.name

