# @ Time    : 2020/5/8 21:27
# @ Author  : JuRan


from exts import db
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime
from markdown import markdown
import bleach

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(db.Model):
    # FrontUser  front_user
    __tablename__ = 'front_user'
    # 安全 asdasd34rsdf  uuid  shortuuid
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)

    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signatrue = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)

    join_time = db.Column(db.DateTime, default=datetime.now)


    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')

        # super(FrontUser, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    read_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("cms_board.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    board = db.relationship("BoardModel", backref="posts")
    author = db.relationship("FrontUser", backref="posts")

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True, attributes=allowed_attrs))

db.event.listen(PostModel.content, 'set', PostModel.on_changed_content)


class CommentModel(db.Model):
    __tablename__ ="comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    post = db.relationship("PostModel", backref="comments")
    author = db.relationship("FrontUser", backref="comments")