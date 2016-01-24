# _*_ coding:utf-8 _*_

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from flask_login import current_user


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

    # 这里不能这样用,因为validate_password函数无法获得email的值,无法对二者是否匹配进行验证
    # def validate_password(self, field):
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if not user.verify_password(field):
    #         raise ValidationError('Wrong password, please try again. ')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, '
                                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match! ')
    ])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ModifyPasswordForm(Form):
    oldpassword = PasswordField('Old password', validators=[DataRequired()])
    newpassword = PasswordField('New password', validators=[
        DataRequired(), EqualTo('newpassword2', message='Password must match! ')
    ])
    newpassword2 = PasswordField('Confirm password', validators=[DataRequired()])
    ok = SubmitField("OK, I'm Sure")

    def validate_oldpassword(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Wrong password, please try again! ')

    def validate_newpassword(self, field):
        if current_user.verify_password(field.data):
            raise ValidationError('New password must be different from the old one! ')


class ChangeEmailForm(Form):
    oldemail = StringField('Old email', validators=[
        DataRequired(), Length(1, 64), Email()])
    newemail = StringField('New email', validators=[
        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    ok = SubmitField("OK, I'm Sure")

    def validate_newemail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Wrong password, please try again. ')





















