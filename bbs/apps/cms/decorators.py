# @ Time    : 2020/5/11 20:51
# @ Author  : JuRan

from flask import session, redirect, url_for, g
from functools import wraps


def login_required(func):
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner


# 装饰器传参数
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inners(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inners
    return outter