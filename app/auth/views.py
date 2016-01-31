# _*_ coding:utf-8 _*_

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm, ModifyPasswordForm, ChangeEmailForm
from ..models import User
from ..email import send_email
import bcrypt
# import json


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # form_login = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            password_hash = user.password_hash.encode("utf-8")
            print password_hash
            if bcrypt.hashpw(form.password.data.encode("utf-8"), password_hash) == password_hash:
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for("auth.login"))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # form_login = LoginForm()
    if form.validate_on_submit():
        password_hash = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt(10))
        user = User(email=form.email.data,
                    username=form.username.data,
                    password_hash=password_hash)
        db.session.add(user)
        db.session.commit()  # 提前提交数据库产生id用于计算token.
        login_user(user, False)
        send_confirmation()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        # flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm')
@login_required
def send_confirmation():
    if not current_user.confirmed:
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=current_user, token=token)
        flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account, Thanks')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


# TODO XXXXXX
@auth.route('/modify-password', methods=['GET', 'POST'])
@login_required
def modify_password():
    form = ModifyPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.newpassword.data
        db.session.add(current_user)
        logout_user()
        flash('You have changed your password, please login again. ')
        return redirect(url_for('auth.login'))
    return render_template('auth/modify_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.cofirmed = False
        current_user.email = form.newemail.data
        send_confirmation()
        flash('You have changed your email address, please confirm your new address.')
        return redirect(url_for('main.index'))
    return render_template('auth/change_email.html', form=form)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    pass
    # send_email(current_user.email, 'Reset Your Password',
    #            'auth/email/reset', user=current_user, token=token)


















