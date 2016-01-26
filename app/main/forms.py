# _*_ coding:utf-8 _*_

from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
# from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email
# from ..models import User


class NameForm(Form):   # flask-wtf 模块需要设置秘钥app.config['SECRET_KEY']='hard to guess string'，以防止跨站请求伪造
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
