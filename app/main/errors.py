from flask import render_template
from forms import LoginForm
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    form_login = LoginForm()
    return render_template('404.html', form_login=form_login), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    form_login = LoginForm()
    return render_template('500.html', form_login=form_login), 500
