# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from flask_babel import gettext
from flask_login import login_required, current_user

from app import db
from . import page
from .forms import PostForm
from .models import Post

from app.blueprints.auth.models import User


@page.route('/', methods=['GET', 'POST'])
@page.route('/index', methods=['GET', 'POST'])
@page.route('/index/<int:page_num>', methods=['GET', 'POST'])
def index(page_num=1):
    posts = Post.query.order_by(Post.created_timestamp.desc()).paginate(
        page_num, 10, False)

    return render_template('default/page/index.html', posts=posts)


@page.route('/<slug>')
def detail_slug(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('default/page/detail.html', post=post)


@page.route('/<int:post_id>')
def detail_post_id(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('default/page/detail.html', post=post)


@page.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You wrote a new post.'), 'success')

        return redirect(url_for('page.detail_slug', slug=post.slug))

    return render_template('default/page/create.html', form=form)


@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)

        db.session.add(post)
        db.session.commit()

        flash(gettext('You edited your post.'), 'success')

        return redirect(url_for('page.detail_slug', slug=post.slug))

    return render_template('default/page/edit.html', form=form, post_id=post_id)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('page.index'))
    else:
        return render_template('default/page/delete.html', form=form, post=post)


@page.route('/user/<username>', methods=['GET', 'POST'])
@page.route('/user/<username>/<int:page_num>', methods=['GET', 'POST'])
def user(username, page_num=1):
    author = User.query.filter(User.username == username).first_or_404()

    posts = Post.query.filter(Post.author == author).order_by(Post.created_timestamp.desc()).paginate(page_num, 10, False)

    return render_template('default/page/user.html', posts=posts)
