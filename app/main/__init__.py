# _*_ coding:utf-8 _*_

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors  # 放在main的定义后是因为views和errors中调用了main
