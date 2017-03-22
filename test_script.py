#-*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from re
import json
import pymysql
def getResponse(url):
    try:
        response = urlopen(url)
    except HTTPError as e:
        return None
    if response == 'null':
        return None
    else: 
        return response.read().decode('utf-8') #还未loads

 
pysql.connect(host='127.0.0.1', unix_soket='/tmp/mysql.sock',
                        user='root', passwd=None, charset='utf8') #password填入root的密码

cur = conn.cursor()
#在本地建立数据库
cur.execute('USE student_card')

orgNameFilter = ['',]
first = 20132100001
last = 2013214857
for (student_id in range(fisrt, last)):
    url = "http://console.ccnu.edu.cn/ecard/getTrans?userId="+str(student_id)+"&days=365&startNum=0&num=10000"
    response = getResponse(url)
    responseJson = json.loads(response)
    for (each_info in responseJson)
        

cur.close()
conn.close()