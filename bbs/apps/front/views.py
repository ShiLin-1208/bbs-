# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan
from flask import Blueprint, views, render_template, make_response, request, session, g, url_for, redirect, g
from utils.captcha import Captcha
from utils import lgcache, restful, safe_url
from io import BytesIO
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from .models import FrontUser, PostModel, CommentModel
from apps.cms.models import BannerModel, BoardModel, HighLightPostModel
from exts import db
from flask_paginate import Pagination, get_page_parameter
from .decorators import login_required
import config
from sqlalchemy.sql import func


front_bp = Blueprint("front", __name__)

from .hooks import before_request

import requests
@front_bp.route("/")
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    board_id =request.args.get('board_id', type=int, default=None)

    sort = request.args.get("st", type=int, default=1)


    #当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*config.PRE_PAGE
    end = start+config.PRE_PAGE
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())

    elif sort == 2:
        # 精华帖子，时间倒叙
        query_obj = db.session.query(PostModel).join(HighLightPostModel)\
            .order_by(HighLightPostModel.create_time.desc())
    elif sort == 3:
        #点赞最多 redis来间隔存储
        # 最新的文章
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 评论数据倒叙
        query_obj = db.session.query(PostModel).join(CommentModel).group_by(
            PostModel.id).order_by(func.count(CommentModel.id).desc())

    if board_id:
        print(board_id)
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()
        # inner_window 内层显示多少个url页码 outer_window 外层显示多少个 下标从0开始
    pagination = Pagination(bs_version=3, page=page, total=total, inner_window=2, outer_window=0,per_page=config.PRE_PAGE)
    # print(pagination.links) #  数据不够时，显示为空   per_page=2

    comment = CommentModel.query.all()
    context ={
        "banners": banners,
        "boards": boards,
        "current_board": board_id,
        "posts":posts,
        "pagination":pagination,
        "current_sort":sort,
        "comment" : comment
    }
    return render_template('front/front_index.html', **context)



@front_bp.route('/captcha/')
def graph_captcha():
    try:
        text, image = Captcha.gene_graph_captcha()
        lgcache.redis_set(text.lower(), text.lower())
        # BytesIO 字节流
        out = BytesIO()
        # 把图片保存在字节流中  并制定格式png
        image.save(out, 'png')
        # 文件流指针
        out.seek(0)
        resp = make_response(out.read())
        resp.content_type = 'image/png'
    except:
        return graph_captcha()
    return resp


@front_bp.route('/test/')
def test():
    return render_template('front/test.html')

#
# class SignupView(views.MethodView):
#
#     def get(self):
#         # 在当前的页面  None
#         # referrer  页面的跳转
#         # http://127.0.0.1:5000/test/ => www.baidu.com
#         # print(request.referrer)
#         return_to = request.referrer
#         # print(safe_url.is_safe_url(return_to))
#         # is_safe_url 请求是否来自站内
#         if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
#             # text, image = Captcha.gene_graph_captcha()
#             # print(text)
#             # print(image)
#             return render_template("front/front_signup.html", return_to=return_to)
#         else:
#             return render_template('front/front_signup.html')
#
#
#     def post(self):
#         form = SignupForm(request.form)
#
#         # 表单验证
#
#         if form.validate():
#             # 保存到数据库
#             telephone = form.telephone.data
#             username = form.username.data
#             password = form.password1.data
#
#             user = FrontUser(telephone=telephone, username=username, password=password)
#
#             if user and user.check_password(password):
#                 session['front_user_id'] = user.id
#                 if remember:
#                     # 持久化
#                     session.permanent = True
#                 return restful.success()
#             else:
#                 return restful.params_errors(message='手机号或者密码错误')
#         else:
#             return restful.params_errors(message=form.get_error())
#

class SignupView(views.MethodView):

    def get(self):
        # 在当前的页面  None
        # referrer  页面的跳转
        # http://127.0.0.1:5000/test/ => www.baidu.com
        # print(request.referrer)
        return_to = request.referrer
        # print(safe_url.is_safe_url(return_to))
        # is_safe_url 请求是否来自站内
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            # text, image = Captcha.gene_graph_captcha()
            # print(text)
            # print(image)
            return render_template("front/front_signup.html", return_to=return_to)
        else:
            return render_template('front/front_signup.html')


    def post(self):
        form = SignupForm(request.form)

        # 表单验证

        if form.validate():
            # 保存到数据库
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errors(message=form.get_error())

class SigninView(views.MethodView):

    def get(self):
        # http://127.0.0.1:5000/signin/
        # print(request.url)  当前的URL地址
        return_to = request.referrer
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')


    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            # user = FrontUser.query.filter(FrontUser.telephone == telephone).first()
            user = FrontUser.query.filter_by(telephone=telephone).first()

            if user and user.check_password(password):
                session['front_user_id'] = user.id
                if remember:
                    # 持久化
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_errors(message='手机号或者密码错误')

        else:
            return restful.params_errors(message=form.get_error())


class PostView(views.MethodView):
    decorators = [login_required]
    def get(self):

        boards = BoardModel.query.all()

        return render_template("front/front_apost.html", boards=boards)
    def post(self):
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data


            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_errors(message="没有这个板块")
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            # return redirect(url_for('front.index'))
            return restful.success()
        else:
            return restful.params_errors(message=form.get_error())

@front_bp.route("/logout/")
def logout():
    del session['front_user_id']
    return redirect(url_for('front.index'))


@front_bp.route("/p/<post_id>/")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if  post == None  :
        return restful.params_errors(message="帖子不存在")
    else:
        post.read_count +=1
        db.session.commit()
        return render_template('front/front_detail.html', post=post)


@front_bp.route("/acomment/", methods=['POST'])
@login_required
def add_comment():
    # 302错误
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errors(message="帖子不存在")
    else:
        return restful.params_errors(message=form.get_error())






front_bp.add_url_rule("/signup/", view_func=SignupView.as_view('signup'))
front_bp.add_url_rule("/signin/", view_func=SigninView.as_view('signin'))
front_bp.add_url_rule("/apost/", view_func=PostView.as_view('apost'))

