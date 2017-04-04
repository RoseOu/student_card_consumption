# coding: utf8
from flask import jsonify
from . import api
from student_card_consumption.models import Page2_data, Page3_data, Page4_data, Page5_data, Student_card_consumption_table

@api.route('/consumption_data/<int:id>', method=['GET'])
def get_all_data(id):
    jsonPage2_obj = Page2_data.query.get_or_404(userId=id).to_json()
    del jsonPage2_obj['userId']
    jsonPage3_obj = Page3_data.query.get_or_404(userId=id).to_json()
    del jsonPage3_obj['userId']
    jsonPage4_obj = Page4_data.query.get_or_404(userId=id).to_json()
    del jsonPage4_obj['userId']
    jsonPage5_obj = Page5_data.query.get_or_404(userId=id).to_json()
    del jsonPage5_obj['userId']

    all_data_page = jsonPage2_obj + jsonPage3_obj + jsonPage4_obj + jsonPage5_obj
    all_data_page['userId'] = id
    
    return jsonify(all_data_page)