#coding:utf-8

from .. import db
import urllib
from ..models import Student,Deal
import json

canteenlist=[
        '华中师范大学/后勤集团/饮食中心/学子餐厅',
        '华中师范大学/后勤集团/饮食中心/东二餐厅',
        '华中师范大学/后勤集团/饮食中心/桂香园餐厅新',
        '华中师范大学/后勤集团/饮食中心/东一餐厅新',
        '华中师范大学/后勤集团/饮食中心/南湖校区餐厅',
        '华中师范大学/后勤集团/饮食中心/博雅园餐厅',
        '华中师范大学/后勤集团/饮食中心/沁园春餐厅',
        '华中师范大学/后勤集团/饮食中心/学子中西餐厅',
        '华中师范大学/后勤集团/商贸中心/蓝色港湾餐厅'
        ]

marketlist=[
        '华中师范大学/后勤集团/商贸中心/超市/学子超市',
        '华中师范大学/校内经营商户/爱心超市',
        '华中师范大学/后勤集团/商贸中心/超市/满江红超市',
        ' 华中师范大学/后勤集团/商贸中心/超市/沁园春超市'
        ]

def get_canteen_deals(student):
    canteen_deals = []
    for deal in student.deals:
        for c in canteenlist:
            if deal.orgName.startswith(c):
                canteen_deals.append(deal)
    return canteen_deals

def canteen_wanton_meal(student):
    canteen_deals = [d for d in get_canteen_deals(student)]
    maxdeal = student.deals[0]
    for cd in canteen_deals:
        if cd.transMoney >= maxdeal.transMoney:
            maxdeal = cd
    datelist = maxdeal.dealDateTime.split()[0].split('-')
    student.CanteenWantonDate = datelist[0]+"年"+str(int(datelist[1]))+"月"+str(int(datelist[2]))+"日"
    student.CanteenWantonCost = round(maxdeal.transMoney,2)
    db.session.add(student)
    db.session.commit()

def canteen_wanton_month(student):
    canteen_deals = [d for d in get_canteen_deals(student)]
    month_dict={9:0.0, 10:0.0, 11:0.0, 12:0.0, 1:0.0, 2:0.0, 3:0.0, 4:0.0, 5:0.0}
    for cd in canteen_deals:
        month = int(cd.dealDateTime.split()[0].split('-')[1])
        if month in month_dict:
            month_dict[month] = month_dict[month] + cd.transMoney
    min_month = min(month_dict.items(), key=lambda x: x[1])
    max_month = max(month_dict.items(), key=lambda x: x[1])
    student.CanteenWantonMonth = max_month[0]
    student.CanteenWantonMonthCost = round(max_month[1],2)
    student.CanteenWantonMul = round(max_month[1]/min_month[1],2) if min_month[1]!=0 else round(max_month[1],2)
    db.session.add(student)
    db.session.commit()

def canteen_total(student):
    canteen_deals = [d for d in get_canteen_deals(student)]
    total_cost = 0.0
    breakfast_cost = 0.0
    lunch_cost = 0.0
    dinner_cost = 0.0
    for cd in canteen_deals:
        total_cost = total_cost + cd.transMoney
        time = int(cd.dealDateTime.split()[1].split(":")[0])
        if time in range(6,10):
            breakfast_cost = breakfast_cost+cd.transMoney
        elif time in range(10,15):
            lunch_cost = lunch_cost+cd.transMoney
        elif time in range(15,23):
            dinner_cost = dinner_cost+cd.transMoney
    student.CanteenTotalCost = round(total_cost,2)
    max_cost = max([breakfast_cost,lunch_cost,dinner_cost])
    if max_cost == breakfast_cost:
        student.CanteenWhatMan = 1
    elif max_cost == lunch_cost:
        student.CanteenWhatMan = 2
    else:
        student.CanteenWhatMan = 3
    db.session.add(student)
    db.session.commit()

def canteen_favorite(student):
    canteen_deals = [d for d in get_canteen_deals(student)]
    cost_dict = {}
    num_dict = {}
    for cd in canteen_deals:
        if cd.orgName in cost_dict:
            cost_dict[cd.orgName] = cost_dict[cd.orgName] + cd.transMoney
            num_dict[cd.orgName] = num_dict[cd.orgName] + 1
        else:
            cost_dict[cd.orgName] = cd.transMoney
            num_dict[cd.orgName] = 1
    max_eat = max(cost_dict.items(), key=lambda x: x[1])
    max_num = num_dict[max_eat[0]]
    max_cost = max_eat[1]
    max_org = max_eat[0].split("/")
    if max_org[-1] in ["一楼","二楼"]:
        max_name = max_org[-2]+max_org[-1]
    else:
        max_name = max_org[-3]+max_org[-2]+max_org[-1]
    student.CanteenFavorite = max_name
    student.CanteenFavoriteNum = max_num
    student.CanteenfavoriteCost = round(max_cost,2)
    db.session.add(student)
    db.session.commit()

def get_market_deals(student):
    market_deals = []
    for deal in student.deals:
        for m in marketlist:
            if deal.orgName.startswith(m):
                market_deals.append(deal)
    return market_deals

def market_wanton_buy(student):
    market_deals = [d for d in get_market_deals(student)]
    deal_dict={}
    for md in market_deals:
        date = md.dealDateTime.split()[0]
        if date in deal_dict:
            deal_dict[date] = deal_dict[date]+md.transMoney
        else:
            deal_dict[date] = md.transMoney
    max_deal = max(deal_dict.items(), key=lambda x: x[1])
    max_date_list = max_deal[0].split('-')
    max_date = max_date_list[0]+"年"+str(int(max_date_list[1]))+"月"+str(int(max_date_list[2]))+"日"
    max_cost = max_deal[1]
    student.MarketWantonDate = max_date
    student.MarketWantonCost = round(max_cost,2)
    db.session.add(student)
    db.session.commit()

def market_total(student):
    market_deals = [d for d in get_market_deals(student)]
    num = 0
    cost  = 0.0
    for md in market_deals:
        num = num+1
        cost = cost+md.transMoney
    student.MarketTotalNum = num
    student.MarketTotalCost = round(cost,2)
    db.session.add(student)
    db.session.commit()

def percent_and_total(student):
    all_deals = [d0 for d0 in student.deals]
    canteen_deals = [d1 for d1 in get_canteen_deals(student)]
    market_deals = [d2 for d2 in get_market_deals(student)]
    all_cost = 0.0
    canteen_cost = 0.0
    market_cost = 0.0
    for ad in all_deals:
        all_cost = all_cost+ad.transMoney
    for cd in canteen_deals:
        canteen_cost = canteen_cost+cd.transMoney
    for md in market_deals:
        market_cost = market_cost+md.transMoney
    canteen_percent = round(canteen_cost/all_cost,4)
    market_percent = round(market_cost/all_cost,4)
    other_percent = round(1.0 - canteen_percent - market_percent,4)
    student.CanteenPercent = canteen_percent
    student.MarketPercent = market_percent
    student.OtherPercent = other_percent
    student.DaysNum = 300
    student.TotalCost = round(all_cost,2)
    db.session.add(student)
    db.session.commit()

def over_and_rank(student):
    order_students = Student.query.order_by(Student.TotalCost.desc()).all()
    student_num = Student.query.count()
    rank = order_students.index(student)+1
    over = round(1-rank/student_num,4)
    student.Over = over
    student.Rank = rank
    db.session.add(student)
    db.session.commit()

def calculate_all():
    for student in Student.query.all():
        canteen_wanton_meal(student)
        canteen_wanton_month(student)
        canteen_total(student)
        canteen_favorite(student)
        market_wanton_buy(student)
        market_total(student)
        percent_and_total(student)
        over_and_rank(student)


