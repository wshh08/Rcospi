from datetime import datetime
from flask import render_template, redirect, url_for

from . import main
from .forms import LoginForm
# from app import db
from ..models import User
from flask_login import login_user


@main.route('/', methods=['GET'])
def index_get():
    form_login = LoginForm()
    return render_template('index.html', current_time=datetime.utcnow(), form_login=form_login)


@main.route('/', methods=['POST'])
def index():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user is not None:
            login_user(user)
            #     return redirect(url_for('.index'))























