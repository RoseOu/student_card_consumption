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
import json
import os

totalStudentAmount = 4857 + 4840 + 4840 + 4642

xrange_list = [xrange(2013210001, 2013210010),
               xrange(2014210001, 2014210010),
               xrange(2015210001, 2015210010), 
               xrange(2016210001, 2016210010)]

#各个年级的xrange
xrange_2013 = xrange(2013210001, 2013214857)
xrange_2014 = xrange(2014210001, 2014214840)
xrange_2015 = xrange(2014210001, 2014214840)
xrange_2016 = xrange(2016210001, 2016214642)
_xrange_list = [xrange_2013, xrange_2014, xrange_2015, xrange_2016]

#其他列表消费点的列表
#除了食堂外的全部
otherlist = [
'/华中师范大学/后勤集团/商贸中心/超市/学子超市',
'/华中师范大学/校内经营商户/爱心超市', 
'/华中师范大学/结账商户/可美克滋', 
'/华中师范大学/后勤集团/商贸中心/超市/满江红超市', 
'/华中师范大学/校内经营商户/阳光咖啡'
]

#真超市列表
#专门指特定的几个超市
ShopList = [
'/华中师范大学/后勤集团/商贸中心/超市/学子超市',
'/华中师范大学/校内经营商户/爱心超市', 
'/华中师范大学/后勤集团/商贸中心/超市/满江红超市', 
]

#获取字典中最大的值
def getTheLargestKeyStr(a_dict):
    temp = 0
    for key in a_dict:
        if a_dict[key] > temp:
            biggestKey = key
            temp = a_dict[key]
    return biggestKey

def getTheLeastKeyStr(a_dict):
    temp = 99999999
    for key in a_dict:
        if a_dict[key] < temp:
            smallestKey = key
            temp = a_dict[key]
    return smallestKey

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

class Student_card_consumption_table(db.Model):
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
    """
    __table_args__ = {'mysql_charset': 'utf8'}
    __tablename__ = "stdcc_table"
    id = db.Column(db.Integer, primary_key=True)
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
                    current_timestamp = datetime.utcnow() + timedelta(hours=8)
                    diff_days = (current_timestamp - datetime(2016,9,1)).days
                    
                    url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='\
                    + str(student_id) + '&days=' + str(diff_days) + '&startNum=0&num=10000'       
                    response = getResponse(url)
                    responseJson = json.loads(response)
                    try:
                        for each_info in responseJson:
                            if (each_info['orgName'][:17] == '华中师范大学/后勤集团/饮食中心') or \
                            each_info['orgName'] == '/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅':
                                #把数据插入数据库
                                User.insert_consumption_data(each_info, student_id)
                            elif each_info['orgName'] in otherlist:
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
        #    #添加新的数据
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
        ························· 
        Col Page2Timestamp: X月X日
        Col Page2singleTransMoney: 共花了XXX元
        Col Page2favOrgName: XXX窗口是你的最爱
        Col Page2favOrgNameCount: 你在此窗口共吃XX顿
        Col Page2favOrgNameTotalTransMoney: 共计消费XX元
        Col Page2totalRefectoryConsumed: 你在食堂共消费XX元
        Col Page2Rian: 你是晨（午,夜）食主义者
        ......................
    """
    __tablename__ = 'page2_data'
    __table_args__ = {'mysql_charset':'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True, index=True)
    Page2Timestamp = db.Column(db.DateTime)        #X月X日
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
                list1 = Student_card_consumption.query.filter_by(userId=student_id).order_by(Student_card_consumption_table.transMoney).all()
                if not list1:
                    break
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
                P2favOrgName = getTheLargestKeyStr(dict1)
                P2favOrgNameCount = dict1[P2favOrgName]
                P2favOrgNameTotalTransMoney = 0
                for i in list2:
                    if i.orgName == P2favOrgName:
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
            

    #@staticmethod
    #def refresh_all_Page2_data():
    #    for grade_xrange in xrange_list:
    #        for student_id in grade_xrange:
    #            list1 = Student_card_consumption.query.filter_by(userId=student_id).order_by(Student_card_consumption_table.transMoney).all()
    #            list2 = []
    #            dict1 = dict() #用于比较此学生在各个餐厅的刷卡数量
    #            for i in list1:
    #                if (i.orgName[:17] == '/华中师范大学/后勤集团/饮食中心') or (i.orgName == "/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅"):
    #                    list2.append(i)
    #            if list2[0].dealDateTimestamp != Page2_data.query.filter_by(userId=student_id).first().Page2Timestamp:
    #                P2singleTransMoney = float(list2[0].transMoney)
    #                P2Timestamp = transSToTS(list2[0].dealDateTimestamp)
    #                u = Page2_data.query.filter_by(userId=student_id).first()
    #                db.session.delete(u)
    #                u.Page2singleTransMoney = P2singleTransMoney
    #                u.Page2Timestamp = P2Timestamp
    #                db.session.add(u)
    #                db.session.commit()
    #
    #           
    #             for i in list2:
    #                 if dict1.has_key(i.orgName):
    #                     dict1[i.orgName] = dict1[i.orgName] + 1
    #                 else:
    #                     dict1.setdefault(i.orgName, default=1)
    #             P2favOrgName = getTheLargestKeyStr(dict1)
    #             P2favOrgNameCount = dict1[P2favOrgName]
    #             P2favOrgNameTotalTransMoney = 0
    #             for i in list2:
    #                 if i.orgName = P2favOrgName:
    #                     P2favOrgNameTotalTransMoney = P2favOrgNameTotalTransMoney + float(i.transMoney)
    #             P2totalRefectoryConsumed = 0
    #             for i in list2:
    #                 P2totalRefectoryConsumed = P2totalRefectoryConsumed + float(i.transMoney)
    #              
    #             morningList = []
    #            noonList = []
    #             eveningList = []
    #             for i in list2:
    #                 dealclock = int(str(transSToTS(i.dealDateTimestamp))[11:13])
    #                 if (dealclock <= 9) and (dealclock >= 6):
    #                     morningList.append(i)
    #                 elif (dealclock >= 11) and (dealclock <= 14):
    #                     noonList.append(i)
    #                 elif (dealclock >= 17) and (dealclock <= 20):
    #                     eveningList.append(
    #             P2Rain = getRain(morningList, noonList, eveningList)
    #
    #             u = Page2_data.query.filter_by(userId=student_id).first()
    #             db.session.delete(u)
    #             u.Page2favOrgName = P2favOrgName
    #             u.Page2favOrgNameCount = P2favOrgNameCount
    #             u.Page2favOrgNameTotalTransMoney = P2favOrgNameTotalTransMoney
    #             u.Page2totalRefectoryConsumed = P2totalRefectoryConsumed
    #             u.Page2Rain = P2Rain 
    #             db.session.add(u)
    #             db.session.commit()
    #    
        def to_json(self):
            json_page2 = {
                'userId' : self.userId,
                'Page2Timestamp' : str(self.Page2Timestamp)[:19],
                'Page2favOrgName' : self.Page2favOrgName,
                'Page2favOrgNameCount' : self.Page2favOrgNameCount,
                'Page2favOrgNameTotalTransMoney' : self.Page2favOrgNameTotalTransMoney,
                'Page2totalRefectoryConsumed' : self.Page2totalRefectoryConsumed,
                'Page2Rain' : self.Page2Rain
            }



class Page3_data(db.Model):
    """
        X月X日在超市疯狂剁手
        挥霍了XX元
        共计在超市刷卡XX次
        累计消费XX元（若数据缺失则在那位用户的界面中不显示此页面）
        ··················
        col userId:学生号
        col Page3Timestamp: X月X日
        col Page3totalTransMoney: 挥霍了XX元
        col Page3totalShoppingCount: 共计才超市刷卡X次
        col Page3totalShoppingConsumed: 累计消费XX元
    """    
    __tablename__ = 'page3_data'
    __table_args__ = {'mysql_charset':'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True, index=True)
    Page3Timestamp = db.Column(db.DateTime)
    Page3totalTransMoney = db.Column(db.Float)
    Page3totalShoppingCount = db.Column(db.Integer)
    Page3totalShoppingConsumed = db.Column(db.Float)

    @staticmethod
    def insert_all_Page3_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                list1 = Student_card_consumption.query.filter_by(userId=student_id).order_by(Student_card_consumption.DateTime.desc()).all()
                if not list1:
                   continue
                list2 = []   #当前学生的所有超市数据
                for i in list1:
                    if i.orgName in otherlist:
                        list2.append(i)
                highestShopTransMoney = float(list2[0].transMoney)
                HSTM_sqlalchemyobj = list2[0]
                for i in list2:
                    if i.transMoney >= HSTM_sqlalchemyobj.transMoney:
                        HSTM_sqlalchemyobj = i
                P3Timestamp = HSTM_sqlalchemyobj.dealDateTimestamp
                P3totalTransMoney = float(HSTM_sqlalchemyobj.transMoney)
                P3totalShoppingCount = len(list2)
                total = 0.0
                for i in list2:
                    total = total + float(i.transMoney)
                P3totalShoppingConsumed = total
                u = Page3_data(userId = student_id,
                               Page3Timestamp = P3Timestamp,
                               Page3totalTransMoney = P3totalTransMoney,
                               Page3totalShoppingCount = P3totalShoppingCount,
                               Page3totalShoppingConsumed = P3totalShoppingConsumed)
                db.session.add(u)
                db.session.commit()

    #这个函数暂时用不到
    @staticmethod
    def refresh_all_Page3_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                #先把已存在的数据删除
                a = Page3_data.query.filter_by(userId=student_id).first()
                db.session.delete(a)
                list1 = Student_card_consumption.query.filter_by(userId=student_id).order_by(Student_card_consumption.DateTime).all()
                list2 = []   #当前学生的所有超市数据
                for i in list1:
                    if i.orgName in otherlist:
                        list2.append(i)
                highestShopTransMoney = float(list2[0].transMoney)
                HSTM_sqlalchemyobj = list2[0]
                for i in list2:
                    if i.transMoney >= HSTM_sqlalchemyobj.transMoney:
                        HSTM_sqlalchemyobj = i
                P3Timestamp = HSTM_sqlalchemyobj.dealDateTimestamp
                P3totalTransMoney = float(HSTM_sqlalchemyobj.transMoney)
                P3totalShoppingCount = len(list2)
                total = 0.0
                for i in list2:
                    total = total + float(i.transMoney)
                P3totalShoppingConsumed = total
                u = Page3_data(userId = student_id,
                               Page3Timestamp = P3Timestamp,
                               Page3totalTransMoney = P3totalTransMoney,
                               Page3totalShoppingCount = P3totalShoppingCount,
                               Page3totalShoppingConsumed = P3totalShoppingConsumed)
                db.session.add(u)
                db.session.commit()
            
        def to_json(self):
            json_Page3 = {
                'userId' : self.userId,
                'Page3Timestamp' : str(self.Page3Timestamp)[:19],
                'Page3totalTransMoney' : self.Page3totalTransMoney,
                'Page3totalShoppingCount' : self.Page3totalShoppingCount,
                'Page3totalShoppingConsumed' : self.Page3totalShoppingConsumed
            }
    

class Page4_data(db.Model):
    """
        你最土豪的月份是：X月
        高达XX元
        竟是最低月份的X倍
        ··································
        col userId: 学生号
        col Page4RichMonthConsum: 最土豪的月份消费的金额
        col Page4RichMonth: 最土豪的月份
        col Page4PoorMonthConsum: 最屌丝月份的消费额诶
        col Page4PoorMonth: 最屌丝的月份
    """
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True)
    Page4RichMonthConsum = db.Column(db.Float)
    Page4PoorMonthConsum = db.Column(db.Float)
    Page4RichMonth = db.Column(db.Integer)
    Page4PoorMonth = db.Column(db.Integer)

    @staticmethod
    def insert_all_Page4_data():
        for xrange_grade in xrangeList:
            for student_id in xrange_grade:
                list1 = Student_card_consumption.query.filter_by(userId=sudent_id).all()
                if not list1:   #如果是空列表则
                    continue
                a_dict = dict()
                monthList [1, 2, 3, 4, 9, 10, 11, 12]
                b_dict = {1:'Jan_total',2:'Feb_total',3:'Mar_total',4:'Apr_total',9:'Sep_total_ly',10:'Oct_total_ly',11:'Nov_total_ly',12:'Dec_total_ly'}
                a_dict['Jan_total'] = [0,1]    #列表中的第一个数值代表月支出，第二个数值是当前月份的数值化
                a_dict['Feb_total'] = [0,2]
                a_dict['Mar_total'] = [0,3]
                a_dict['Apr_total'] = [0,4]
                a_dict['Sep_total_ly'] = [0,9]      #ly == last year
                a_dict['Oct_total_ly'] = [0,10]
                a_dict['Nov_total_ly'] = [0,11]
                a_dict['Dec_total_ly'] = [0,12]
                for i in list1:
                    month = int(str(i.dealDateTimestamp)[6:8])
                    if month in monthList:
                        a_dict[b_dict[month]][0] = a_dict[b_dict[month]][0] + float(i.transMoney)

                #找出12个变量中最大的那个
                #找出12个变量中最小的那个
                maxkey = getTheLargestKeyStr(a_dict)
                minkey = getTheLeastKeyStr(a_dict)
    
                P4RichMonth = a_dict['maxkey'][1]#最大的那个变量名
                P4PoorMonth = a_dict['minkey'][1]#最小的那个变量名
                P4RichMonthConsum = a_dict[maxkey][0]
                P4PoorMonthConsum = a_dict[minkey][0]
                
                u = Page4_data(userId = student_id,
                               Page4RichMonthConsum = P4RichMonth,
                               Page4PoorMonthConsum = P4PoorMonth,
                               Page4RichMonth = P4PoorMonth,
                               Page4PoorMonth = P4PoorMonth)
                db.session.add(u)
                db.session.commit()
    
    def to_json(self):
        return {
            'userId': self.userId,
            'Page4RichMonthConsum' : self.Page4RichMonthConsum,
            'Page4PoorMonthConsum' : self.Page4PoorMonthConsum,
            'Page4PoorMonth' : self.Page4PoorMonth,
            'Page4RichMonth' : self.Page4RichMonth
        }


class Page5_data(db.Model):
    """
        你在近一年XX天（日期从上学期开始到现在）内共消费了XXX元
        超过了全校XX%的人 全校排名XXX
        可以有一个饼图分别给出超市、食堂、其他分别消费占的比例
       （直接在饼图各部分加上他所占的百分比，旁边列出饼图不同颜色分别代表超市食堂其他）
       ········································
       col Page5totalTransMoney: 共消费了XXX元
       col Page5totalRefectoryTransMoney: 食堂消费总共额度
       col Page5totalShopTransMoney: 超市消费的总共额度
       col Page5RankTheWholeSchool: 全校消费排名
    """

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, unique=True)
    Page5totalTransMoney = db.Column(db.Float)
    Page5totalRefectoryTransMoney = db.Column(db.Float)
    Page5totalShopTransMoney = db.Column(db.Float)
    Page5RankTheWholeSchool = db.Column(db.Integer, default=None)

    @staticmethod
    def insert_all_page5_data():
        for grade_xrange in xrange_list:
            for student_id in grade_xrange:
                list1 = Student_card_consumption_table.query.filter_by(userId=student_id).all()
                if not list1:
                    continue
                totalTransMoney = 0.0
                for i in list1:
                    totalTransMoney = totalTransMoney + float(i.transMoney)
                totalRefectoryTransMoney = 0.0
                for i in list1:
                    if (i.orgName[:17] == '/华中师范大学/后勤集团/饮食中心') or (i.orgName == "/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅"):
                       totalRefectoryTransMoney = totalRefectoryTransMoney + float(i.transMoney)
                
                totalShopTransMoney = 0.0
                for i in list1:
                    if i.orgName in ShopList:
                        totalShopTransMoney = totalShopTransMoney + float(i.transMoney)
                u = Page5_data(
                    userId = student_id,
                    Page5totalTransMoney = totalTransMoney,
                    Page5totalRefectoryTransMoney = totalRefectoryTransMoney,
                    Page5totalShopTransMoney = totalShopTransMoney,
                )
                db.session.add(u)
                db.session.commit()
    
    @staticmethod
    def insertAllRanking():
        list1 = Page5_data.query.order_by(Page5_data.Page5totalTransMoney.asc()).all
        for xrange_grade in xrange_list:
            for student_id in xrange_grade:
                Page5_obj = Page5_data.query.filter_by(userId=student_id).first()
                if not Page5_obj:
                    continue
                db.session.delete(Page5_obj)
                Page5_obj.Page5RankTheWholeSchool = list1.index(Page5_obj) + 1
                db.session.add(Page_obj)
                db.session.commit()
                
    
    def to_json(self):
        return  {
            'userId' : self.UserId,
            'Page5totalTransMoney' : self.Page5totalTransMoney, 
            'Page5totalRefectoryTransMoney' : self.Page5totalRefectoryTransMoney,
            'Page5totalShopTransMoney' : self.Page5totalShopTransMoney,
            'Page5RankTheWholeSchool' : self.Page5RankTheWholeSchool
        }
