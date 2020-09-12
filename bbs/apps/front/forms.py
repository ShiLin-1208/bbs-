# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo, Regexp
from utils import lgcache


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确的手机号')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确的短信验证码')])
    username = StringField(validators=[Length(min=2, max=20, message='请输入正确的用户名')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确的密码')])
    password2 = StringField(validators=[EqualTo('password1', message='两次密码输入不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确的图形验证码')])


    def validate_sms_captcha(self, field):
        telephone = self.telephone.data
        sms_captcha = self.sms_captcha.data

        # 从Redis中取验证码
        sms_captcha_redis = lgcache.redis_get(telephone)

        if not sms_captcha_redis or sms_captcha_redis.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')


    def validate_graph_captcha(self, field):
        graph_captcha = self.graph_captcha.data

        graph_captcha_redis = lgcache.redis_get(graph_captcha)

        if not graph_captcha_redis or graph_captcha_redis.lower() != graph_captcha.lower():
            raise ValidationError(message='图形验证码错误')



class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确的手机号')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确的密码')])
    remember = StringField(InputRequired())


class AddPostForm(BaseForm):
    title= StringField(validators=[InputRequired(message="请输入标题")])
    board_id = IntegerField(validators=[InputRequired(message="请选择板块")])
    content = StringField(validators=[InputRequired(message="请输入内容")])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确的图形验证码')])
    def validate_graph_captcha(self, field):
        graph_captcha = self.graph_captcha.data

        graph_captcha_redis = lgcache.redis_get(graph_captcha)

        if not graph_captcha_redis or graph_captcha_redis.lower() != graph_captcha.lower():
            raise ValidationError(message='图形验证码错误')



class AddCommentForm(BaseForm):
    content =StringField(validators=[InputRequired(message="请输入评论内容")])
    post_id = IntegerField(validators=[InputRequired(message="请选择一篇帖子")])
