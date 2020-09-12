# @ Time    : 2020/5/11 20:54
# @ Author  : JuRan

from flask import request, url_for, redirect, session, g
from .views import cms_bp
from .models import CMSUser, CMSPersmission
# from apps.cms.views import cms_bp


# 通过钩子函数
@cms_bp.before_request
def before_request():

    if not request.path.endswith(url_for('cms.login')):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('cms.login'))

    if 'user_id' in session:
        user_id = session.get('user_id')
        user = CMSUser.query.get(user_id)
        # print(CMSUser.query.filter(CMSUser.email == 'admin@qq.com').first())
        if user:
            g.cms_user = user


@cms_bp.context_processor
def cms_context_processor():
    return {"CMSPersmission": CMSPersmission}


# 获取到用户传过来的权限
