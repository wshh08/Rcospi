# _*_ coding:utf-8 _*_

import os
from flask_bootstrap import WebCDN, StaticCDN, ConditionalCDN

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        pass

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string.'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Rcosπ]-'
    FLASKY_MAIL_SENDER = 'Rcosπ Admin <wshh08@126.com>'  # 外发邮件时的同一发件地址，必须与SMTP服务器配置相容（wshh08@rcospi不行）.
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  # 管理员收件地址
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        # 以下配置flask-bootstrap使用cdn.bootcss.com的CDN服务，防止被墙。。
        # bootStrap/css&js
        cdn_base_url = WebCDN('//cdn.bootcss.com/bootstrap/3.3.5/')
        local = StaticCDN('bootstrap.static', rev=True)
        cdn_conditional = ConditionalCDN('BOOTSTRAP_SERVE_LOCAL', local, cdn_base_url)
        app.extensions['bootstrap']['cdns']['bootstrap'] = cdn_conditional

        # jQuery
        cdn_base_url = WebCDN('//cdn.bootcss.com/jquery/2.1.3/')
        cdn_conditional = ConditionalCDN('BOOTSTRAP_SERVE_LOCAL', local, cdn_base_url)
        app.extensions['bootstrap']['cdns']['jquery'] = cdn_conditional


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'flasky-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'flasky-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'flasky.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}














