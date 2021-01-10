from flask import Blueprint, request, make_response, jsonify, abort, url_for, g
from ..utils.sql import db
from ..model.user import User
from flask_httpauth import HTTPBasicAuth
from flask_cors import cross_origin

# us = Blueprint('us', __name__, url_prefix='/api/user')
us = Blueprint('us', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@us.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)  # 跨域
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    elif User.query.filter_by(username=username).first() is not None:
        user = User.query.filter_by(username=username).first()
        if user.verify_password(password):
            return (jsonify({'username': user.username}),
                    {'Location': url_for('us.get_user', id=user.id, _external=True)})
        else:
            abort(400)

    else:
        abort(400)  # do not existing user


@us.route('/api/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def new_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    if username is None or email is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username, email=email)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 200,
            {'Location': url_for('us.get_user', id=user.id, _external=True)})


@us.route('/api/users/<int:id>')
@cross_origin(supports_credentials=True)
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@us.route('/api/token')
@cross_origin(supports_credentials=True)
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.encode('utf-8').decode('ascii'), 'duration': 600})


from ..utils.mail import send_reset_password_email, get_random_code


@us.route('/api/getcode', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_code():
    username = request.json.get('username')
    email = request.json.get('email')
    if email is None or username is None:
        return jsonify({'message': '请输入手机号和邮箱'})
    elif User.query.filter_by(username=username, email=email).first() is None:
        return jsonify({'message': '请输入正确的手机号和邮箱'})  # do not existing user
    else:
        code = get_random_code()
        token = User.get_reset_password_token(code, 600)
        send_reset_password_email(email, code=code)
        return jsonify({'message': '发送成功', "token": token.encode('utf-8').decode('ascii')})


@us.route('/api/reset-password', methods=['POST'])
@cross_origin(supports_credentials=True)
def reset_password():
    try:
        username = request.json.get('username')
        email = request.json.get('email')
        code = request.json.get('code')
        password = request.json.get('password')
        token = request.json.get('token')
    except Exception:
        return jsonify({'message': '请输入正确的信息'})
    if email is None or username is None or code is None or password is None:
        return jsonify({'message': '更改失败'})
    elif User.query.filter_by(username=username, email=email).first() is None:
        return jsonify({'message': '更改失败'})
    if User.verify_reset_password_code_token(code, token):
        user = User.query.filter(User.username == username).first()
        user.hash_password(password)
        db.session.commit()
        return jsonify({'message': '更改成功'})
    else:
        return jsonify({'message': '更改失败,请输入正确的验证码'})


@us.route('/api/resource')
@cross_origin(supports_credentials=True, methods=['POST'])
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
