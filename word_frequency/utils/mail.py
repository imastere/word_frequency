from flask_mail import Message, Mail
from flask import render_template

from ..manage import app

mail = Mail()
# 邮箱配置
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '1209974170@qq.com'  # 邮箱账号
app.config['MAIL_PASSWORD'] = 'mkjgoydzmezmjegf'  # QQ邮箱授权码 # QQ邮箱->设置->账户->[POP3...]->生成授权码->发送短信->获取授权码
mail.init_app(app)


def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject,
        sender=app.config['MAIL_USERNAME'],
        recipients=[to])
    # 发送一封HTML邮件
    mail.html = render_template(template, kwargs)
    mail.send(msg)


# 发送重置密码
def send_reset_password_email(to, code):
    msg = Message(
        body="更改密码的验证码为" + code + "有效期为1分钟",
        sender=app.config['MAIL_USERNAME'],
        recipients=[to])
    # 发送一封HTML邮件
    mail.send(msg)


from random import choice

# 生成随机验证码
str_num = "1234567890"


def get_random_code():
    code = ''
    for i in range(4):
        code = code + choice(str_num)
    return code


def generate_token(self, expiration=600):
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    s = Serializer(secret_key=app.config['SECRET_KEY'], expires_in=expiration)
    # s.dumps生成的是byte数组，我们需要编码成字符串
    return s.dumps({'id': self.id}).decode('utf-8')
