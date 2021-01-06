import jwt as jwt

from ..utils.sql import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from ..manage import app
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
import time

# Flask 使用类似的方式处理 cookies 的。这个实现依赖于一个叫做 itsdangerous 的库，我们这里也会采用它。
# 为了创建密码散列，我将会使用 PassLib 库，一个专门用于密码散列的 Python 包。
# PassLib 提供了多种散列算法供选择。custom_app_context 是一个易于使用的基于 sha256_crypt 的散列算法。
# 出于安全原因，用户的原始密码将不被存储，密码在注册时被散列后存储到数据库中。使用散列密码的话，如果用户数据库不小心落入恶意攻击者的手里，他们也很难从散列中解析到真实的密码。
# 密码 决不能 很明确地存储在用户数据库中。
app.config['SECRET_KEY'] = 'imastere is very handsome'
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
           {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])
