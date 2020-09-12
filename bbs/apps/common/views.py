# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan

from utils import send_msg, restful
from flask import Blueprint, request, jsonify
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils import lgcache
from qiniu import Auth, put_file, etag
import qiniu.config


common_bp = Blueprint("common", __name__, url_prefix='/c')


# 只要到当前的请求 就会发生短信
# @common_bp.route("/sms_captcha/", methods=['POST'])
# def sms_captcha():
#     telephone = request.form.get('telephone')
#
#     if not telephone:
#         return restful.params_errors(message='请填写手机号码')
#
#     captcha = Captcha.gene_text(number=4)
#
#     if send_msg.send_mobile_msg(telephone, captcha) == 0:
#         return restful.success()
#     else:
#         return restful.params_errors(message='发送失败')


@common_bp.route("/sms_captcha/", methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)


    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        # print("发送的验证码{}".format(captcha))
        print(send_msg.send_mobile_msg(telephone, captcha))

        if send_msg.send_mobile_msg(telephone, captcha) == 0:

            lgcache.redis_set(telephone, captcha)

            return restful.success()
        else:

            return restful.params_errors(message='发送失败')

    else:
        return restful.params_errors(message='参数错误')


@common_bp.route("/uptoken/")
def uptoken():
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'Pq9naz_G-zMSGq0SzRkKgb9au1puctwOTzJ9yHqo'
    secret_key = 'jvgL4iJl45XhSIFzieZPlS4rNwPOIBKOhwvps2mO'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    bucket_name = 'logic-juran'

    token = q.upload_token(bucket_name)

    return jsonify({"uptoken": token})
