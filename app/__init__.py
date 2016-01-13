# _*_ coding:utf-8 _*_

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from configs import config
from flask_login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 通过导入蓝本添加路由和自定义的错误页面
    # from .main import main as main_blueprint 必须放在db=SQLAlchemy后面，防止views中
    # import db时循环依赖错误
    from .main import main as main_blueprint  # 将此句放入create_app()函数的定义内部，
    # 这样在import db时就不会需要回到main/__init__.py去执行views.py而造成循环依赖错误啦。。。
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

print "Test Import"
print "Test Again"










