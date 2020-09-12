# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from wtforms import Form
from wtforms import StringField
from wtforms.validators import InputRequired, regexp
import hashlib


class SMSCaptchaForm(Form):
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    # 验证前端发送过来的sign和后端加密之后的sign 是否一致

    def validate_sign(self, field):
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # 服务端加密之后生成的
        sign2 = hashlib.md5((timestamp + telephone + 'q3423805gdflvbdfvhsdoa`#$%').encode('utf-8')).hexdigest()

        # print("客户端sign %s" % sign)
        # print("服务端sign %s" % sign2)

        if sign == sign2:
            return True
        else:
            return False





