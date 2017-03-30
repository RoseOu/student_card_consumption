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
from urllib import urlopen
from datetime import datetime, timedelta
#from pytz import timezone
from ..manage import current_table
import json

#各个年级的xrange
xrange_2013 = xrange(2013210001, 2013214857),
xrange_2014 = xrange(2014210001, 2014214840),
xrange_2015 = xrange(2014210001, 2014214840),
xrange_2016 = xrange(2016210001, 2016214642)
xrange_list = [xrange_2013, xrange_2014, xrange_2015, xrange_2016]

shopList = [
'/华中师范大学/后勤集团/商贸中心/超市/学子超市',
'/华中师范大学/校内经营商户/爱心超市', 
'/华中师范大学/结账商户/可美克滋', 
'/华中师范大学/后勤集团/商贸中心/超市/满江红超市', 
'/华中师范大学/校内经营商户/阳光咖啡'
]

#获取字典中最大的值
def getTheBiggestKey(a_dict):
    temp = 0
    for key in a_dict:
        if a_dict[key] > temp:
            biggestKey = key
    return biggestKey

def transSToTS(Timestamp_str):
    Timestamp = datetime(int(Timestamp_str[:4]),
                         int(Timestamp_str[5:7]),
                         int(Timestamp_str[8:10]),
                         int(Timestamp_str[11:13]),
                         int(Timestamp_str[14:16]),
                         int(Timestamp_str[17:])
                         ),
    return Timestamp
def getResponse(url):
    try:
        response = urlopen(url)
    except HTTPError as e:
        return None
    if response == 'null':
        return None
    else:
        return response.read().decode('utf-8')

def getRain(MorningList, NoonList, EveningList):
    Morning_consumed = 0
    Noon_consumed = 0
    Evening_consumed = 0
    for i in MorningList:
        Morning_consumed = Morning_consumed + float(i.transMoney)
    for i in NoonList:
        Noon_consumed = Noon_consumed + float(i.transMoney)
    for i in EveningList:
        Evening_consumed = Evening_consumed + float(i.transMoney)
    if (Morning_consumed >= Evening_consumed) and (Morning_consumed >= Noon_consumed):
        return "breakfastrain"
    elif Noon_consumed >= Evening_consumed:
        return "lunchrain"
    else:
        return "dinnerain"
class Student_card_consumption_table1(db.Model):
    """
        Student_card_consumption_table1: 学生卡消费信息

        :var id: 主键 
        :var userName: 学生姓名
        :var dealTime: 交易当天发生的时间点
        :var dealDate: 交易发生的日期
        :var dealTimestamp: 交易的timestamp
        :var userId: 学生学号
        :var transMoney: 交易的金额

        :func insert_all_consumption_data
        :func refresh_all_consumption_data        把新的数据添加到数据库中,删除旧的数据(一年以前的)
    """
    __table_args__ = {'mysql_charset': 'utf8'}
    __tablename__ = "stdcc_table1"
    id = db.Column(db.Integer, primery_key=True)
    userId = db.Column(db.Integer)
    orgName = db.Column(db.String(50))
    userName = db.Column(db.String(20))
    dealDateTimestamp = db.Column(db.DateTime, index=True)
    dealDate = db.Column(db.String(20))
    dealTime = db.Column(db.String(20))
    transMoney = db.Column(db.Float)

    #插入消费数据
    @staticmethod
    def insert_all_consumption_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                    url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='\
                    + str(student_id) + '&days=365&startNum=0&num=10000'
                    response = getResponse(url)
                    responseJson = json.loads(response)
                    try:
                        for each_info in responseJson:
                            if (each_info['orgName'][:17] == '华中师范大学/后勤集团/饮食中心') or \
                            each_info['orgName'] == '/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅':
                                #把数据插入数据库
                                User.insert_consumption_data(each_info, student_id)
                            elif each_info['orgName'] in shopList:
                                User.insert_consumption_data(each_info, student_id)
                    except TypeError as e:
                        continue
    @staticmethod
    def insert_consumption_data(each_info, userId):     #userId为int型
        Timestamp_str = each_info['dealDateTime']
        data = Student_card_consumption_table2(userId = userId,
                                        orgName = each_info['orgName'],
                                        dealDateTimestamp = datetime(int(Timestamp_str[:4]),
                                                                     int(Timestamp_str[5:7]),
                                                                     int(Timestamp_str[8:10]),
                                                                     int(Timestamp_str[11:13]),
                                                                     int(Timestamp_str[14:16]),
                                                                     int(Timestamp_str[17:])
                                                                     ),
                                        userName = each_info['userName'],
                                        dealDate = Timestamp_str[:10],
                                        dealTime = Timestamp_str[11:],
                                        transMoney = float(each_info['transMoney'])
                                        )
        db.session.add(data)
        db.session.commit()


        #@staticmethod
        #def refresh_all_consumption_data():
        #    CurrentLocalTimestamp = datetime.utcnow() + timedelta(hours=8)               #野蛮式时间转换
        #    CurrentLocalTimestamp_aYearAgo = CurrentLocalTimestamp - timedelta(days=365) #野蛮式计算一年前时间 
            #添加新的数据
        #    for grade_xrange in xrange_list:
        #        for student_id in grade_xrange:
        #            url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='\
        #            + str(student_id) + '&days=365&startNum=0&num=50'  
        #            response = getResponse(url)
        #            responseJson = json.loads(response)
        #            try:
        #                for each_info in responseJson:
        #                    if ((each_info['orgName'][:17] == '华中师范大学/后勤集团/饮食中心') or \
        #                    each_info['orgName'] == '/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅') and :

            #删除旧的数据
        #    Last100_data = Student_card_consumption.order_by


    def __repr__(self):
        return "<Student_card_consumption %r>" % self.id     #???


class Student_card_consumption_table2(db.Model):
    """
        Student_card_consumption_table1的拷贝: 学生卡消费信息
    """
    __table_args__ = {'mysql_charset': 'utf8'}
    __tablename__ = "stdcc_table2"
    id = db.Column(db.Integer, primery_key=True)
    userId = db.Column(db.Integer)
    orgName = db.Column(db.String(50))
    userName = db.Column(db.String(20))
    dealDateTimestamp = db.Column(db.DateTime, index=True)
    dealDate = db.Column(db.String(20))
    dealTime = db.Column(db.String(20))
    transMoney = db.Column(db.Float)

    #插入消费数据
    @staticmethod
    def insert_all_consumption_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                    url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='\
                    + str(student_id) + '&days=365&startNum=0&num=10000'
                    response = getResponse(url)
                    responseJson = json.loads(response)
                    try:
                        for each_info in responseJson:
                            if (each_info['orgName'][:17] == '华中师范大学/后勤集团/饮食中心') or \
                            each_info['orgName'] == '/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅':
                                #把数据插入数据库
                                User.insert_consumption_data(each_info, student_id)
                            elif each_info['orgName'] in shopList:
                                User.insert_consumption_data(each_info, student_id)
                    except TypeError as e:
                        continue

    @staticmethod
    def insert_consumption_data(each_info, userId):     #userId为int型
        Timestamp_str = each_info['dealDateTime']
        data = Student_card_consumption_table2(userId = userId,
                                        orgName = each_info['orgName'],
                                        dealDateTimestamp = datetime(int(Timestamp_str[:4]),
                                                                     int(Timestamp_str[5:7]),
                                                                     int(Timestamp_str[8:10]),
                                                                     int(Timestamp_str[11:13]),
                                                                     int(Timestamp_str[14:16]),
                                                                     int(Timestamp_str[17:])
                                                                     ),
                                        userName = each_info['userName'],
                                        dealDate = Timestamp_str[:10],
                                        dealTime = Timestamp_str[11:],
                                        transMoney = float(each_info['transMoney'])
                                        )
        db.session.add(data)
        db.session.commit()

class Page2_data(db.Model):
    """
        Private_data: 学生个人信息(7页数据的收集)
        ``````````````````````
        第二页

        X月X日
        你在食堂吃了最放肆的一顿
        共花了XXX元
        XXX窗口（刷卡次数最多的窗口）是你的最爱
        在此窗口共吃XX顿，共计消费XX元
        你在食堂共消费XX元，早（中晚）餐消费最高，你可能是晨（午、夜）食主义者   
        ...................... 
    """
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True, index=True)
    Page2Timestamp = db.Column(db.DateTime)       #X月X日
    Page2singleTransMoney = db.Column(db.Float)    #共花费了
    Page2favOrgName = db.Column(db.String(30))
    Page2favOrgNameCount = db.Column(db.Integer)
    Page2favOrgNameTotalTransMoney = db.Column(db.Integer)
    Page2totalRefectoryConsumed = db.Column(db.Float)
    Page2Rian = db.Column(db.String(15))
    
    @staticmethod
    def insert_all_Page2_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                #获取最大学生单次消费的记录
                list1 = current_table.query.filter_by(userId=student_id).order_by(current_table.transMoney).all()
                list2 = []
                dict1 = dict() #用于比较此学生在各个餐厅的刷卡数量
                for i in list1:
                    if (i.orgName[:17] == '/华中师范大学/后勤集团/饮食中心') or (i.orgName == "/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅"):
                        list2.append(i)
                P2singleTransMoney = float(list2[0].transMoney)
                P2Timestamp = transSToTS(list2[0].dealDateTimestamp)
                for i in list2:
                    if dict1.has_key(i.orgName):
                        dict1[i.orgName] = dict1[i.orgName] + 1
                    else:
                        dict1.setdefault(i.orgName, default=1)
                P2favOrgName = getTheBiggestKey(dict1)
                P2favOrgNameCount = dict1[P2favOrgName]
                P2favOrgNameTotalTransMoney = 0
                for i in list2:
                    if i.orgName = P2favOrgName:
                        P2favOrgNameTotalTransMoney = P2favOrgNameTotalTransMoney + float(i.transMoney)
                P2totalRefectoryConsumed = 0
                for i in list2:
                    P2totalRefectoryConsumed = P2totalRefectoryConsumed + float(i.transMoney)
                
                morningList = []
                noonList = []
                eveningList = []
                for i in list2:
                    dealclock = int(str(transSToTS(i.dealDateTimestamp))[11:13])
                    if (dealclock <= 9) and (dealclock >= 6):
                        morningList.append(i)
                    elif (dealclock >= 11) and (dealclock <= 14):
                        noonList.append(i)
                    elif (dealclock >= 17) and (dealclock <= 20):
                        eveningList.append(i)

                P2Rain = getRain(morningList, noonList, eveningList)
                u = Page2_data(
                            userId = student_id,
                            Page2Timestamp = P2Timestamp,
                            Page2singleTransMoney = P2singleTransMoney,
                            Page2favOrgName = P2favOrgName,
                            Page2favOrgNameCount = P2favOrgNameCount,
                            Page2favOrgNameTotalTransMoney = P2favOrgNameTotalTransMoney,
                            Page2totalRefectoryConsumed = P2totalRefectoryConsumed,
                            Page2Rain = P2Rain
                )
                db.session.add(u)
                db.session.commit()
            

    @staticmethod
    def refresh_all_Page2_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                list1 = current_table.query.filter_by(userId=student_id).order_by(current_table.transMoney).all()
                list2 = []
                dict1 = dict() #用于比较此学生在各个餐厅的刷卡数量
                for i in list1:
                    if (i.orgName[:17] == '/华中师范大学/后勤集团/饮食中心') or (i.orgName == "/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅"):
                        list2.append(i)
                if list2[0].dealDateTimestamp != Page2_data.query.filter_by(userId=student_id).first().Page2Timestamp:
                    P2singleTransMoney = float(list2[0].transMoney)
                    P2Timestamp = transSToTS(list2[0].dealDateTimestamp)
                    u = Page2_data.query.filter_by(userId=student_id).first()
                    db.session.delete(u)
                    u.Page2singleTransMoney = P2singleTransMoney
                    u.Page2Timestamp = P2Timestamp
                    db.session.add(u)
                    db.session.commit()

               
                 for i in list2:
                     if dict1.has_key(i.orgName):
                         dict1[i.orgName] = dict1[i.orgName] + 1
                     else:
                         dict1.setdefault(i.orgName, default=1)
                 P2favOrgName = getTheBiggestKey(dict1)
                 P2favOrgNameCount = dict1[P2favOrgName]
                 P2favOrgNameTotalTransMoney = 0
                 for i in list2:
                     if i.orgName = P2favOrgName:
                         P2favOrgNameTotalTransMoney = P2favOrgNameTotalTransMoney + float(i.transMoney)
                 P2totalRefectoryConsumed = 0
                 for i in list2:
                     P2totalRefectoryConsumed = P2totalRefectoryConsumed + float(i.transMoney)
                  
                 morningList = []
                 noonList = []
                 eveningList = []
                 for i in list2:
                     dealclock = int(str(transSToTS(i.dealDateTimestamp))[11:13])
                     if (dealclock <= 9) and (dealclock >= 6):
                         morningList.append(i)
                     elif (dealclock >= 11) and (dealclock <= 14):
                         noonList.append(i)
                     elif (dealclock >= 17) and (dealclock <= 20):
                         eveningList.append(
                 P2Rain = getRain(morningList, noonList, eveningList)

                 u = Page2_data.query.filter_by(userId=student_id).first()
                 db.session.delete(u)
                 u.Page2favOrgName = P2favOrgName
                 u.Page2favOrgNameCount = P2favOrgNameCount
                 u.Page2favOrgNameTotalTransMoney = P2favOrgNameTotalTransMoney
                 u.Page2totalRefectoryConsumed = P2totalRefectoryConsumed
                 u.Page2Rain = P2Rain 
                 db.session.add(u)
                 db.session.commit()
        
        def to_json(self):
            json_page2 = {
                'id' = self.id,
                'userId' = self.userId,
                'Page2Timestamp' = str(self.Page2Timestamp)[:19],
                'Page2favOrgName' = self.Page2favOrgName,
                'Page2favOrgNameCount' = self.Page2favOrgNameCount,
                'Page2favOrgNameTotalTransMoney' = self.Page2favOrgNameTotalTransMoney,
                'Page2totalRefectoryConsumed' = self.Page2totalRefectoryConsumed,
                'Page2Rain' = self.Page2Rain
            }



class Page3_data(db.Model):
    """
        X月X日在超市疯狂剁手
        挥霍了XX元
        共计在超市刷卡XX次
        累计消费XX元（若数据缺失则在那位用户的界面中不显示此页面）
    """    
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True, index=True)
    Page3Timestamp = db.Column(db.DateTime)
    Page3maxTransMoney = db.Column(db.Float)
    Page3totalShopingCount = db.Column(db.Integer)
    Page3
    Page3 

class Page4_data(db.Model):
    """
        你最土豪的月份是：X月
        高达XX元
        竟是最低月份的X倍
    """
    id = db.Column(db.Integer, primary_key=True)


class Page5_data(db.Model):
    """
        你在近一年XX天（日期从上学期开始到现在）内共消费了XXX元
        超过了全校XX%的人 全校排名XXX
        可以有一个饼图分别给出超市、食堂、其他分别消费占的比例（直接在饼图各部分加上他所占的百分比，旁边列出饼图不同颜色分别代表超市食堂其他 ）
    """
    


class Public_data(db.Model):
    """
        弹出图片图片内容
        1.华师包子哪家强
        XX食堂XX窗口：日营业额：XXX 刷卡数目：XXX
        （ 排名前三的窗口）
        2.华师食堂日营额大揭秘
        东一食堂：XXX元
        东二食堂：XXX元
        学子食堂：XXX元
        。。。。
        按照钱数量的多少排名
        3.早餐华师最火爆的窗口
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        4.午餐华师最热门的窗口
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        6.晚餐大家都喜欢去的窗口
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX

        7.华师面食大比拼
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
        XXX食堂XX窗口：刷卡数量XXX日营业额XXX
    """
