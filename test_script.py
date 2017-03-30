#-*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import pymysql
import datetime
def getResponse(url):
    try:
        response = urlopen(url)
    except HTTPError as e:
        return None
    if response == 'null':
        return None
    else: 
        return response.read().decode('utf-8') #还未loads


 
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                        user='root', passwd=None, charset='utf8') #password填入root的密码,默认密码为空

cur = conn.cursor()
#在本地建立数据库
cur.execute('USE student_card')

def insertInfoIntoDB(each_info, userId):
    cur.execute("INSERT INTO student_card_consumption (transMoney,\
                                                       orgName,\
                                                       userName,\
                                                       userId,\
                                                       dealDate,\
                                                       dealDateTimestamp,\
                                                       dealTime) VALUES (%s, %s, %s, %s, '%s', '%s', '%s')",
                 (each_info["transMoney"],
                  each_info["orgName"],
                  each_info["userName"],
                  str(userId)),
                  each_info["dealDateTime"][:9],
                  each_info["dealDateTime"]
                  each_info["dealDateTIme"][11:])
    conn.commit
    
    
#测试用
first = 20132100001
last = 2013214857

shopList = ['/华中师范大学/后勤集团/商贸中心/超市/学子超市', '/华中师范大学/校内经营商户/爱心超市', '/华中师范大学/结账商户/可美克滋', 
            '/华中师范大学/后勤集团/商贸中心/超市/满江红超市', '/华中师范大学/校内经营商户/阳光咖啡']
for student_id in xrange(first, last):
    url = "http://console.ccnu.edu.cn/ecard/getTrans?userId="+str(student_id)+"&days=365&startNum=0&num=10000"
    response = getResponse(url)
    responseJson = json.loads(response)
    try:
        for each_info in responseJson:
            if (each_info['orgName'][:17] == '华中师范大学/后勤集团/饮食中心/') or \
            each_info['orgName'] == '/华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅':   #想用正则表达式
                #把这一条信息保存到数据
                insertInfoIntoDB(each_info, str(student_id))
            else if each_info['orgName'] in shopList:
                insertInfoIntoDB(each_info, str(student_id))
    except TypeError as e:
        continue
        

cur.close()
conn.close()