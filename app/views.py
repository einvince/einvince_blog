# -*- coding: UTF-8 -*-   
from . import main
from .. import db
from flask import render_template, redirect, url_for, abort, flash, request,current_app
from flask.ext.login import login_required, current_user
from .forms import LoginForm, RegisterForm, PostArticle
from ..models import Content, User, Role
import markdown2
from misaka import Markdown, HtmlRenderer

# 定义路由
@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Content.query.order_by(Content.pub_time.desc()).paginate(
        page, per_page=10, error_out=False)
    contents = pagination.items
    # contents = Content.query.order_by(Content.pub_time.desc()).all()

    return render_template('index.html', contents=contents, pagination=pagination)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = None
    password = None
    remember_me = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('邮箱或者密码不正确')
        #flash('电子邮箱或密码不正确')
    form.email.data = ''
    return render_template('login.html', form=form, email=email, password=password, remember_me=remember_me)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('index'))


@main.route('/post-article', methods=['GET', 'POST'])
@login_required
def post_article():
    form = PostArticle()
    if form.validate_on_submit():
        content = Content(title=form.title.data,
                          body=form.body.data,
                          category=form.category.data,
                          abstract=form.abstract.data,
                          pub_time=form.pub_time.data,)
        db.session.add(content)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('post-article.html', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    content = Content.query.get_or_404(id)
    form = PostArticle()
    if form.validate_on_submit():
        content.title = form.title.data
        content.body = form.body.data
        content.abstract = form.abstract.data
        content.category = form.category.data
        content.pub_time = form.pub_time.data
        db.session.commit()
        flash('你已经更新')
        return redirect(url_for('index'))
    form.body.data = content.body
    form.title.data = content.title
    form.abstract.data = content.abstract
    form.category.data = content.category
    form.pub_time.data = content.pub_time
    return render_template('post-article.html', form=form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    content = Content.query.get_or_404(id)
    if content is None:
        flash('文章不存在')
        return redirect(url_for('index'))
    db.session.delete(content)
    db.session.commit()
    flash('已删除该文章')
    return redirect(url_for('admin.html'))

@main.route('/article/<int:id>')
def article(id):
    content = Content.query.get_or_404(id)
    return render_template('article.html', content=content)

@main.route('/category/<xxx>')
def category(xxx):
    categorys = Content.query.fliter_by(category=xxx).all()
    return render_template('category.html', categorys=categorys)

@main.route('/admin.html', methods=['GET', 'POST'])
@login_required
def admin():
    contents = Content.query.order_by(Content.pub_time.desc()).all()
    return render_template('admin.html', contents=contents)

@main.route('/resume')
def resume():
    return send_from_directory("static", "resume.pdf")

@main.route('/search/<keyword>', methods=['GET'])
def search(keyword):
    return redirect('http://www.google.com/search?q=site:' + config.site_url + ' ' + keyword)


'''
@main.route('/resume')
def resume():
    return render_template('resume.html')
'''
