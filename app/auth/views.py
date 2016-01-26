# _*_ coding:utf-8 _*_

from flask import render_template, session, redirect, request, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm, ModifyPasswordForm, ChangeEmailForm
from ..models import User
from ..email import send_email
import json
import rsa


@auth.route('/ajax/login', methods=['POST'])
def login_ajax():
    js = json.dumps(request.get_json())
    js = json.loads(js)
    # email = js.get('email')
    # password = js.get('password')
    rejson = {'email': js.get('email'),
              'password': js.get('password')}
    resopnse = jsonify(rejson)
    resopnse.set_cookie('username', js.get('email'))
    return resopnse


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误')
    return render_template('auth/login.html', form=form, form_login=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for("auth.login"))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
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


















