# _*_ coding:utf-8 _*_
from flask import request, jsonify
from flask_login import login_user
from . import ajax
from ..models import User


@ajax.route('/pre_login', methods=['POST'])
def login_ajax_confirm():
    email = request.json.get('email')
    # sa = ''
    # rejson = {}
    print email
    user = User.query.filter_by(email=email).first()
    if user is not None:
        sa = user.password_hash[0:29]
        rejson = {'result': True,
                  'sa': sa}
    else:
        sa = ''
        rejson = {'result': False,
                  'sa': sa}
    resopnse = jsonify(rejson)
    # resopnse.set_cookie('sa', sa)
    return resopnse


@ajax.route('/login', methods=['POST'])
def login_ajax():
    result = False
    js = request.json
    # print request.cookies request.cookies是一个字典.
    # print type(js) dict!!!
    # js = request.get_json() 此句结果和上一句一样，都是返回一个json对象(就是dict ?).
    # js = json.dumps(request.get_json()) dumps将dict数据dump成str
    # js = json.loads(js)　loads将str还原成dict
    # email = js.get('email')
    # password = js.get('password')
    # rejson = {'email': js.get('email'),
    #           'hash': js.get('hash')}
    email = js.get('email')
    ha = js.get('ha')
    user = User.query.filter_by(email=email).first()
    if user is not None:
        psw_hash = user.password_hash
        if psw_hash == ha:
            login_user(user, True)
            result = True
    else:
        result = False
    rejson = {'result': result}
    resopnse = jsonify(rejson)
    # resopnse.set_cookie('username', js.get('email'))
    return resopnse
