# @ Time    : 2020/5/25 22:06
# @ Author  : JuRan

from qiniu import Auth, put_file, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = ''
secret_key = ''
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'lgcoder-image'

# 上传后保存的文件名
key = 'my-python-logo.png'

# 生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

# 要上传文件的本地路径
localfile = r'D:\Python进阶班\Flask框架\bbs\static\common\images\logo.png'

ret, info = put_file(token, key, localfile)
print('ret', ret)
print('info', info)

assert ret['key'] == key
assert ret['hash'] == etag(localfile)
