# -*- coding: UTF-8 -*-   
from . import db , login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin


class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    pub_time = db.Column(db.DateTime)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    abstract = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    def __repr__(self):
        return "<Content %r>" % self.title

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('密码是不可读取的类型')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = "categorys"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    count = db.Column(db.Integer)
    contents = db.relationship("Content", backref="category")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))