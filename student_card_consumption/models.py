#coding:utf-8
"""
    models.py
"""
from . import db
import urllib
from datetime import datetime, timedelta
import json
import os

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key=True)
    studentid = db.Column(db.Integer,default=0,unique=True,index=True)
    name = db.Column(db.String(64),default="")
    deals = db.relationship('Deal', backref='student', lazy='dynamic', cascade='all')
    CanteenWantonDate = db.Column(db.String(64),default="")
    CanteenWantonCost = db.Column(db.Float,default=0.0)
    CanteenWantonMonth = db.Column(db.Integer,default=0)
    CanteenWantonMonthCost = db.Column(db.Float,default=0.0)
    CanteenWantonMul = db.Column(db.Float,default=0.0)
    CanteenTotalCost = db.Column(db.Float,default=0.0)
    CanteenWhatMan = db.Column(db.Integer,default=0)
    CanteenFavorite = db.Column(db.String(128),default="")
    CanteenFavoriteNum = db.Column(db.Integer,default=0)
    CanteenfavoriteCost = db.Column(db.Float,default=0.0)
    MarketWantonDate = db.Column(db.String(64),default="")
    MarketWantonCost = db.Column(db.Float,default=0.0)
    MarketTotalNum = db.Column(db.Integer,default=0)
    MarketTotalCost = db.Column(db.Float,default=0.0)
    CanteenPercent = db.Column(db.Float,default=0.0)
    MarketPercent = db.Column(db.Float,default=0.0)
    OtherPercent = db.Column(db.Float,default=0.0)
    DaysNum = db.Column(db.Integer,default=0)
    TotalCost = db.Column(db.Float,default=0.0)
    Over = db.Column(db.Float,default=0.0)
    Rank = db.Column(db.Integer,default=0)

    def __repr__(self):
        return "<Student %r>" % self.id

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer,primary_key=True)
    dealDateTime = db.Column(db.String(64))
    orgName = db.Column(db.String(128))
    transMoney = db.Column(db.Float)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id',ondelete="CASCADE"))

    def __repr__(self):
        return "<Deal %r>" % self.id



