# @ Time    : 2020/5/20 21:35
# @ Author  : JuRan

from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient


def send_mobile_msg(mobile, code):
    # 初始化client,apikey作为所有请求的默认值
    clnt = YunpianClient('e8abe129a4e9f9a7c8c9adc8ece9ebc9')
    param = {YC.MOBILE: mobile, YC.TEXT: '【御城领】您的验证码是{}'.format(code)}
    r = clnt.sms().single_send(param)
    print(r.data())
    print(r.msg())
    return r.code()


# print(send_mobile_msg('18646175117', '123'))



# 0 发送成功
# print(r.code())
# 发送成功的消息
# print(r.msg())
#
# print(r.data())
# 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
# 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()
