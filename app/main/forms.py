# _*_ coding:utf-8 _*_

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):   # flask-wtf 模块需要设置秘钥app.config['SECRET_KEY']='hard to guess string'，以防止跨站请求伪造
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')
