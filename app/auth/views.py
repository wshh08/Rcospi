# _*_ coding:utf-8 _*_

from flask import render_template, session, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm, ModifyPasswordForm
from ..models import User
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误')
    return render_template('auth/login.html',
                           form=form)


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


@auth.route('/modifypassword', methods=['GET', 'POST'])
@login_required
def modify():
    form = ModifyPasswordForm()
    if form.validate_on_submit() and not current_user.verify_password(form.newpassword.data):
        current_user.password = form.newpassword.data
        db.session.add(current_user)
        logout_user()
        flash('You have changed your password, please login again. ')
        return redirect(url_for('auth.login'))
    elif form.validate_on_submit() and current_user.verify_password(form.newpassword.data):
        flash('New password must be <b>different</b> from old password, please try again!')
    else:
        return redirect('auth.modify')
    return render_template('auth/modify.html', form=form)

















