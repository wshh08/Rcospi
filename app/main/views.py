from datetime import datetime
from flask import render_template, redirect, url_for

from . import main
from .forms import NameForm
from app import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html', current_time=datetime.utcnow())























