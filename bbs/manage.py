# @ Time    : 2020/5/8 21:24
# @ Author  : JuRan
from flask_script import Manager
from bbs import app
from flask_migrate import Migrate, MigrateCommand
from exts import db
# 导入模型
from apps.cms.models import CMSUser, CMSRole, CMSPersmission, BannerModel, BoardModel, HighLightPostModel
from apps.front.models import FrontUser, PostModel, CommentModel
import random

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print("前台用户添加成功")




@manager.command
def create_role():
    # 访问者
    visitor = CMSRole(name='访问者', desc='只能查看数据,不能修改数据')
    visitor.permissions = CMSPersmission.VISITOR

    # 运营人员
    operator = CMSRole(name='运营', desc='管理帖子,管理评论,管理前台用户')
    operator.permissions = CMSPersmission.VISITOR | CMSPersmission.POSTER | CMSPersmission.CMSUSER | CMSPersmission.COMMENTER | CMSPersmission.FRONTUSER

    # 管理员
    admin = CMSRole(name='管理员', desc='拥有本系统大部分权限')
    admin.permissions = CMSPersmission.VISITOR | CMSPersmission.POSTER | CMSPersmission.CMSUSER | CMSPersmission.COMMENTER | CMSPersmission.FRONTUSER | CMSPersmission.BOARDER

    # 开发人员
    developer = CMSRole(name='开发者', desc='拥有所有的权限')
    developer.permissions = CMSPersmission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.command
def test_permission():
    user = CMSUser.query.get(3)
    # print(user)
    if user.has_permission(CMSPersmission.VISITOR):
        print("这个用户有访问者的权限")
    else:
        print("这个用户没有访问者的权限")


# 用户添加到角色里面
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色成功")
        else:
            print("角色不存在")
    else:
        print("邮箱不存在")

@manager.command
def create_text_post():
    for i in range(1,200):
        title = "标题 %s" %i
        content = "内容 %s" %i
        author =FrontUser.query.first()
        post = PostModel(title=title, content=content)
        post.author=author
        post.board_id = random.randint(1,6)
        db.session.add(post)
        db.session.commit()
    print("帖子添加成功")


if __name__ == '__main__':
    manager.run()