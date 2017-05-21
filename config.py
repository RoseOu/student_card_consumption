# coding: utf-8
"""
    config.py
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    配置基类
        密钥配置、SQLALCHEMY配置
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I like flask'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """
    development configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('STDCC_MYSQL_URI')

class ProductionConfig(Config):
    """
    production configuration
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    @classmethod
    def init_app(cls,app):
        Config.init_app(app)

class TestingConfig(Config):
    """
    testing configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-test.sqlite")


config = {
    'develop' : DevelopmentConfig,
    'product' : ProductionConfig,
    'testing' : TestingConfig,
    'default' : DevelopmentConfig
}
