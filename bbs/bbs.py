# @ Time    : 2020/5/8 21:22
# @ Author  : JuRan

from flask import Flask
from exts import db, mail
from apps.cms.views import cms_bp
from apps.front.views import front_bp
from apps.common.views import common_bp
import config
from flask_wtf import CSRFProtect


# 前台 front
# 后台 cms  用户模型
# 共有的 common

app = Flask(__name__)

CSRFProtect(app)


app.config.from_object(config)

db.init_app(app)
mail.init_app(app)


app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)


if __name__ == '__main__':
    app.run(debug=True)