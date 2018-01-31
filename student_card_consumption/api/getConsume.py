# coding: utf8
from flask import jsonify
from . import api
from ..models import Student

@api.route('/consumption/test/', methods=['GET'])
def test():
    return jsonify({
        "hi":"hi"
        })

@api.route('/consumption/<int:id>/', methods=['GET'])
def get_consumption(id):
    student = Student.query.filter_by(studentid=id).first()
    return jsonify({
        "CanteenWantonDate":student.CanteenWantonDate,
        "CanteenWantonCost":student.CanteenWantonCost,
        "CanteenWantonMonth":student.CanteenWantonMonth,
        "CanteenWantonMonthCost":student.CanteenWantonMonthCost,
        "CanteenWantonMul":student.CanteenWantonMul,
        "CanteenTotalCost":student.CanteenTotalCost,
        "CanteenWhatMan":student.CanteenWhatMan,
        "CanteenFavorite":student.CanteenFavorite,
        "CanteenFavoriteNum":student.CanteenFavoriteNum,
        "CanteenfavoriteCost":student.CanteenfavoriteCost,
        "MarketWantonDate":student.MarketWantonDate,
        "MarketWantonCost":student.MarketWantonCost,
        "MarketTotalNum":student.MarketTotalNum,
        "MarketTotalCost":student.MarketTotalCost,
        "CanteenPercent":student.CanteenPercent,
        "MarketPercent":student.MarketPercent,
        "OtherPercent":student.OtherPercent,
        "DaysNum":student.DaysNum,
        "TotalCost":student.TotalCost,
        "Over":student.Over,
        "Rank":student.Rank
    })
