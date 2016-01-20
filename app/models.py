# _*_ coding:utf-8 _*_

from . import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):  # 3600s
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])  # 用于解码的s不需要设置一样的expiration，只要"秘钥"一样就可以用来解码
        if s.loads(token).get('confirm') == self.id:
            self.confirmed = True
            db.session.add(self)
            return True
        else:
            # print type(s.loads(token).get('confirm'))
            # print type(self.id)
            # print self.id == s.loads(token).get('confirm')
            return False

        # try:
        #     data = s.load(token)
        # except Exception, e:  # 此句有问题导致捕获“'str' object has no attribute 'read'”错误引起‘return false’.
        #     print Exception, ":", e
        #     return False
        # if data.get('confirm') != self.id:
        #     return False
        # self.confirmed = True
        # db.session.add(self)
        # return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))























