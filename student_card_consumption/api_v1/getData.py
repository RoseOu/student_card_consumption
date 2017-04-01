# coding: utf8
from flask import jsonify
from . import api
from student_card_consumption.models import Page2_data, Page3_data, Page4_data,
            Page5_data,Public_data
from ...manage import current_table

@api.route('/page2/<int:id>', methods=['GET'])
def get_page2_data(id):
    u = Page2_data.query.get_or_404(userId=id)
    return jsonify(u.to_json())

@api.route('/page3/<int:id>', methods=['GET'])
def get_page3_data(id):
    u = Page3_data.query.get_or_404(userId=id)
    return jsonify(u)

@api.route('/page4/<int:id>', methods=['GET'])
def get_page4_data(id):
    u = Page4_data.query.get_or_404(userId=id)
    return jsonify(u)

@api.route('/page5/<int:id>', methods=['GET'])
def get_page5_data(id):
    u = Page5_data.query.get_or_404(userId=id)
    return jsonify(u)

@api.route('/public_data', methods=['GET'])
def get_public_data():
    
