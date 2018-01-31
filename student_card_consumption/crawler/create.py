#coding:utf-8

from .. import db
import urllib
import urllib2
from ..models import Student,Deal
import json

#studentnum=4857+4840+4594+4642

#student2013=range(2013210001, 2013214858)
#student2014=range(2014210001, 2014214841)
#student2015=range(2015210001, 2015214595)
#student2016=range(2016210001, 2016214643)
#student2017=range(2017210001, 2017214917)

#studentlist = [student2014,student2015,student2016,student2017]

def create_students(studentlist):
    for sl in studentlist:
        for studentid in sl:
            if not Student.query.filter_by(studentid=studentid).first():
                url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='+str(studentid)+'&days=300&startNum=0&num=1'
                dicrequest=urllib2.Request(url)
                dicresponse=urllib2.urlopen(dicrequest)
                dicthtml = dicresponse.read()
                dictjson = json.loads(dicthtml)
                if dictjson:
                    student = Student()
                    student.studentid = studentid
                    student.name = dictjson[0]['userName']
                    db.session.add(student)
                    db.session.commit()
                    print "add 1 student!"


def create_deals(studentlist):
    for sl in studentlist:
        for studentid in sl:
            if Student.query.filter_by(studentid=studentid).first():
                url = 'http://console.ccnu.edu.cn/ecard/getTrans?userId='+str(studentid)+'&days=400&startNum=0&num=3650'
                dicrequest=urllib2.Request(url)
                dicresponse=urllib2.urlopen(dicrequest)
                dicthtml = dicresponse.read()
                dictjson = json.loads(dicthtml)
                if dictjson:
                    student = Student.query.filter_by(studentid=studentid).first()
                    for d in dictjson:
                        if d['dealTypeName'] == u"消费":
                            if int(d['dealDateTime'].split()[0].split('-')[0])==2017:
                                deal = Deal()
                                deal.dealDateTime = d['dealDateTime']
                                deal.orgName = d['orgName']
                                deal.transMoney = d['transMoney']
                                deal.student = student
                                db.session.add(deal)
                                db.session.commit()
                        print "add 1 student deal!"

