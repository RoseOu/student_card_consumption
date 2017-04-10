# coding: utf-8
"""
    error.py
    `````````
    : HTTP 错误处理
"""
from flask import jsonify


def not_found(message):
    response = jsonify({'error': 'not_found', 'message': message})
    response.status_code = 404
    return response

def server_error(message):
    response = jsonify({'error': 'server_error', 'message': message})
    response.status_code = 500
    return response