# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo, URL
from utils import lgcache



class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

#
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请出入正确的邮箱地址'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


# 表单提交上来的数据 是否符合要求
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='密码长度有误')])
    newpwd = StringField(validators=[Length(6, 20, message='密码长度有误')])
    # 两次密码输入是否一致
    newpwd2 = StringField(validators=[EqualTo("newpwd", message="两次密码输入不一致")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    captcha = StringField(validators=[Length(min=4, max=4, message='请输入正确长度的验证码')])


    def validate_captcha(self, field):
        # 表单提交上的验证码
        captcha = self.captcha.data
        email = self.email.data

        # 取redis中保存的验证码
        redis_captcha = lgcache.redis_get(email)

        if not redis_captcha or captcha.lower() != redis_captcha.lower():
            raise ValidationError('邮箱验证码错误')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入图片链接'), URL(message='图片链接有误')])
    link_url = StringField(validators=[InputRequired(message='请输入跳转链接'), URL(message='跳转链接有误')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])



class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='轮播图不存在')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='板块不存在')])

