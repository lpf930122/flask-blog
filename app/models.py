from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    posts =db.relationship('Post', backref='author', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)                             #评论ID
    body = db.Column(db.Text)                                                #评论内容
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  #评论时间
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))             #评论人ID
    path = db.Column(db.String(256), index=True)                             #评论路径枚举



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    hide = db.Column(db.Boolean)


class Tag(db.Model):
    __tagname__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)  #标签ID
    tag = db.Column(db.String(64))  #标签内容
    post_id = db.Column(db.Integer, index=True) #标签父ID


