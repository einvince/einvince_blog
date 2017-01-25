# -*- coding: UTF-8 -*-
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField,DateField
from wtforms.validators import Required, Email, Length
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField


class LoginForm(Form):
    email = StringField(u'电子邮箱:', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'密码:', validators=[Required()])
    submit = SubmitField(u'提交')

class PostArticle(Form):
    title = StringField(u'标题', validators=[Required()])
    body = PageDownField(u'正文', validators=[Required()])
    abstract = TextAreaField(u'简介', validators=[Required()])
    category = StringField(u'分类', validators=[Required()])
    pub_time = DateField(u'时间')
    submit = SubmitField(u'发表')
