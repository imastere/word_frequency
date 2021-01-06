from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()

from flask_sqlalchemy import SQLAlchemy  # 使用 Flask-SQLAlchemy 来构建用户数据库模型并且存储到数据库中。
from ..manage import app

# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xiaoxiao@localhost/word_project'
# 设置是否跟踪数据库的修改情况，一般不跟踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 数据库操作时是否显示原始SQL语句，一般都是打开的，因为我们后台要日志
app.config['SQLALCHEMY_ECHO'] = True

# 实例化orm框架的操作对象，后续数据库操作，都要基于操作对象来完成
db = SQLAlchemy(app)
