#coding:utf-8

from .. import db
import urllib.request
from ..models import Student,Deal
import json

#studentnum=4857+4840+4594+4642

#student2013=range(2013210001, 2013214858)
#student2014=range(2014210001, 2014214841)
#student2015=range(2015210001, 2015214595)
#student2016=range(2016210001, 2016214643)
#student2017=range(2017210001, 2017214917)

#test3=range(2013210001, 2013210006)
#test4=range(2014210001, 2014210006)
#test5=range(2015210001, 2015210006)
#test6=range(2016210001, 2016210006)
#test7=range(2017210001, 2017210006)

#studentlist = [student2014,student2015,student2016,student2017]

#testlist = [test4,test5]

def create_students(studentlist):
    for sl in studentlist:
        for studentid in sl:
            if not Student.query.filter_by(studentid=studentid).first():
                url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='+str(studentid)+'&days=300&startNum=0&num=1'
                dicthtml = urllib.request.urlopen(url)
                dicthtml1 = dicthtml.read()
                dictjson = json.loads(dicthtml1)
                if dictjson:
                    student = Student()
                    student.studentid = studentid
                    student.name = dictjson[0]['userName']
                    db.session.add(student)
                    db.session.commit()
                    print("add 1 student!")


def create_deals(studentlist):
    for sl in studentlist:
        for studentid in sl:
            if Student.query.filter_by(studentid=studentid).first():
                url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='+str(studentid)+'&days=300&startNum=0&num=3000'
                dicthtml = urllib.request.urlopen(url)
                dicthtml1 = dicthtml.read()
                dictjson = json.loads(dicthtml1)
                if dictjson:
                    student = Student.query.filter_by(studentid=studentid).first()
                    for d in dictjson:
                        if d['dealTypeName'] == "消费":
                            deal = Deal()
                            deal.dealDateTime = d['dealDateTime']
                            deal.orgName = d['orgName']
                            deal.transMoney = d['transMoney']
                            deal.student = student
                            db.session.add(deal)
                            db.session.commit()
                    print("add 1 student deal!")
