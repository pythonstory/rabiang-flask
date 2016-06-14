# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash

from app import db
from app.utils.html import slugify
from . import page
from .forms import PostForm
from .models import Post


@page.route('/', methods=['GET', 'POST'])
@page.route('/index', methods=['GET', 'POST'])
@page.route('/index/<int:pos>', methods=['GET', 'POST'])
def index(pos=1):
    posts = Post.query.paginate(1, 10, False).items

    return render_template('default/page/index.html', posts=posts)


@page.route('/<slug>')
def detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('default/page/detail.html', post=post)


@page.route('/<int:pid>')
def detail_pid(pid):
    post = Post.query.filter(Post.id == pid).first_or_404()
    return render_template('default/page/detail.html', post=post)


@page.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.slug = slugify(post.title)

        db.session.add(post)
        db.session.commit()

        flash('You wrote a new post.')

        return redirect(url_for('page.detail', slug=post.slug))

    return render_template('default/page/create.html', form=form)


@page.route('/edit/<int:pid>', methods=['GET', 'POST'])
def edit(pid):
    post = Post.query.get_or_404(pid)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        post.slug = slugify(post.title)

        db.session.add(post)
        db.session.commit()

        flash('You edited your post.')

        return redirect(url_for('page.detail', slug=post.slug))

    return render_template('default/page/edit.html', form=form)


@page.route('/delete/<int:pid>', methods=['GET', 'POST'])
def delete(pid):
    if request.method == 'POST':
        pass
    else:
        pass
