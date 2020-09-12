# @ Time    : 2020/5/11 20:51
# @ Author  : JuRan

from flask import session, redirect, url_for, g
from functools import wraps

def login_required(func):
    # @wraps(func)
    def inner(*args, **kwargs):
        if 'front_user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))
    return inner
