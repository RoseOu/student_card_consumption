"""
    STDCC_config.py 
    ```````````````
    
    : student_card_consumption backend configuration file
    : --Config:       配置基类
    : --DevConfig:    开发环境配置
    : --TestConfig:   测试环境配置
    : --ProConfig:    生产环境配置
    ................. 
    : copyright: (c) 2017 MuxiStudio
    : license: MIT
"""

import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    配置基类
        密钥配置、SQLALCHEMY配置
    """
    MUXIAUTH = 'http://user.muxixyz.com'                          #Do I need to use this?
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I like flask'   #Do I need to use this?
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    """
    开发环境下配置
        开启调试器
        数据库采用mysql数据库 //sqlite也行吧
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('STDCC_ORM_URI')

class TestConfig(Config):
    """
    测试环境下的配置
    """
    DEBUG = True

class ProConfig(Config):
    """
    生产环境下的配置
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("STDCC_ORM_URI")

config = {
    'develop' : DevConfig, 
    'product' : ProConfig,
    'testing' : TestConfig,
    'default' : DevConfig
}