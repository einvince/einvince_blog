# -*- coding: UTF-8 -*-
from . import main
from .. import db
from flask import render_template, redirect, url_for, abort, flash, request,current_app
from flask.ext.login import login_required, login_user, logout_user
from .forms import LoginForm, PostArticle
from ..models import Content, User ,Category

# 定义路由
@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Content.query.order_by(Content.pub_time.desc()).paginate(
        page, per_page=5, error_out=False)
    contents = pagination.items
    categorys=Category.query.order_by(Category.count)
    return render_template('index.html', contents=contents, pagination=pagination,categorys=categorys)


@main.route('/login', methods=['GET', 'POST'])
def login():
    print("in----")
    with open("bug.txt","a+") as f:
        try:
            form = LoginForm()
            email = None
            password = None
            remember_me = None
            if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                if user is not None and user.verify_password(form.password.data):
                    login_user(user)
                    return redirect(request.args.get('next') or url_for('main.index'))
                else:
                    flash('error')
            form.email.data = ''
            return render_template('login.html', form=form, email=email, password=password, remember_me=remember_me)
            # raise Exception('spam', 'eggs')
        except Exception as e:
            f.write(str(e)+'\n')
        


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('main.index'))


@main.route('/post-article', methods=['GET', 'POST'])
@login_required
def post_article():
    form = PostArticle()
    if form.validate_on_submit():
        print form.category.data
        category=Category.query.filter_by(tag=form.category.data).first()
        if category is None:
            category=Category(tag=form.category.data,count=1)
        else:
            category.count=int(category.count)+1
        content = Content(title=form.title.data,
                          body=form.body.data,
                          abstract=form.abstract.data,
                          pub_time=form.pub_time.data,category=category)
        db.session.add(category)
        db.session.add(content)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post-article.html', form=form)




@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    content = Content.query.get_or_404(id)
    form = PostArticle()
    if form.validate_on_submit():
        category=Category.query.filter_by(tag=form.category.data).first()
        content.title = form.title.data
        content.body = form.body.data
        content.abstract = form.abstract.data
        content.category = category
        content.pub_time = form.pub_time.data
        db.session.commit()
        flash('你已经更新')
        return redirect(url_for('main.admin'))
    form.body.data = content.body
    form.title.data = content.title
    form.abstract.data = content.abstract
    form.category.data = content.category.tag
    form.pub_time.data = content.pub_time
    return render_template('post-article.html', form=form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    content = Content.query.get_or_404(id)
    if content is None:
        flash('文章不存在')
        return redirect(url_for('main.index'))
    db.session.delete(content)
    db.session.commit()
    flash('已删除该文章')
    return redirect(url_for('main.admin'))

@main.route('/article/<int:id>')
def article(id):
    content = Content.query.get_or_404(id)
    return render_template('article.html', content=content)

@main.route('/category/<tag>')
def category(tag):
    tagname=tag
    category=Category.query.filter_by(tag=tag).first()
    contents=category.contents
    return render_template("category.html",contents=contents,tagname=tagname,category=category)




@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    contents = Content.query.order_by(Content.pub_time.desc()).all()
    return render_template('admin.html', contents=contents)


'''
@main.route('/resume')
def resume():
    return render_template('resume.html')
'''
