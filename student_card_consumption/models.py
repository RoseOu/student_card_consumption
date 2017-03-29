# coding: utf-8
"""
    models.py
    `````````
    : SQL数据库模块
    :  -- student_card_consumption        学生卡数据库的拷贝
    
    .......... 
    : copyright: (c) 2017 by MuxiStudio
    : license: MIT
"""

from . import db
import base64


class Student_card_consumption(db.Model):
    """
        Student_card_consumption: 学生卡消费信息

        :var id: 主键 
        :var userName: 学生姓名
        :var dealTime: 交易当天发生的时间点
        :var dealDate: 交易发生的日期
        :var dealTimestamp: 交易的timestamp
        :var userId: 学生学号
        :var transMoney: 交易的金额
    """
    __table_args__ = {'mysql_charset': 'utf8'}
    __tablename__ = "std_cc"
    id = db.Column(db.Integer, primery_key=True)
    userId = db.Column(db.Integer)
    orgName = db.Column(db.String(50))
    userName = db.Column(db.String(20))
    dealDateTimestamp = db.Column(db.DateTime, index=True)
    dealDate = db.Column(db.String(20))
    dealTime = db.Column(db.String(20))
    transMoney = db.Column(db.Float)

