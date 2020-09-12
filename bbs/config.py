# @ Time    : 2020/5/8 21:23
# @ Author  : JuRan
import os

HOSTNAME = '127.0.0.1'
DATABASE = 'flask_bbs'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'root'

DB_URL = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# engine = create_engine(DB_URL)
SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SECRET_KEY = os.urandom(15)

SECRET_KEY = 'asd23asdfsdf'

# 发送邮箱的服务地址  QQ邮箱
MAIL_SERVER = 'smtp.qq.com'
# 端口465或587
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False  465

MAIL_USERNAME = '844297347@qq.com'
# 不是QQ密码
MAIL_PASSWORD = 'imzrvumjpzdfeceh'
MAIL_DEFAULT_SENDER = '2096842618@qq.com'

TEMPLATES_AUTO_RELOAD = True
PRE_PAGE = 2

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

