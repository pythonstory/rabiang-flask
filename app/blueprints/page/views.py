# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash

from app import db
from app.utils.html import slugify
from . import page
from .forms import PostForm
from .models import Post


@page.route('/', methods=['GET', 'POST'])
@page.route('/index', methods=['GET', 'POST'])
@page.route('/index/<int:page_num>', methods=['GET', 'POST'])
def index(page_num=1):
    posts = Post.query.paginate(page_num, 2, False)

    return render_template('default/page/index.html', posts=posts)


@page.route('/<slug>')
def detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('default/page/detail.html', post=post)


@page.route('/<int:post_id>')
def detail_post_id(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
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


@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        post.slug = slugify(post.title)

        db.session.add(post)
        db.session.commit()

        flash('You edited your post.')

        return redirect(url_for('page.detail', slug=post.slug))

    return render_template('default/page/edit.html', form=form)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    if request.method == 'POST':
        pass
    else:
        pass
