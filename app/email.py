# _*_ coding:utf-8 _*_

from flask_mail import Message
from . import mail
from manage import app
from flask import render_template
from decorators import async


@async
def send_async_email(msg):
    # flask-mail需要读取app context中的config设置值
    # 利用with app.app_context()语句可生成一个AppContext对象
    # 并通过AppContext的push()函数绑定到当前上下文.
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    send_async_email(msg)
