# @ Time    : 2020/5/15 20:41
# @ Author  : JuRan

import redis


# 把验证码存到Redis
# 取
# 删除

# 连接Redis
# decode_responses = True 默认取出来的数据就是字符串
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def redis_set(key, value, timeout=60):
    return r.set(key, value, timeout)


def redis_get(key):
    return r.get(key)


def redis_delete(key):
    return r.delete(key)


# if __name__ == '__main__':
#     print(redis_set('name', 'juran'))
#     # 二进制
#     print(redis_get('name'))


