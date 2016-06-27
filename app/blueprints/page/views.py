# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, \
    current_app
from flask_babel import gettext
from flask_login import login_required, current_user

from app import db
from app.blueprints.auth.models import User
from . import page
from .forms import PostForm, CommentForm
from .models import Post, Comment, Tag, post_tags


def sidebar_data():
    sidebar = {}

    recent_posts = Post.query \
        .order_by(Post.created_timestamp.desc()) \
        .limit(current_app.config.get('RABIANG_RECENT_POSTS')) \
        .all()

    sidebar['recent_posts'] = recent_posts

    recent_comments = Comment.query \
        .order_by(Comment.created_timestamp.desc()) \
        .limit(current_app.config.get('RABIANG_RECENT_COMMENTS')) \
        .all()

    sidebar['recent_comments'] = recent_comments

    top_tags = Tag.query \
        .add_columns(db.func.count(Tag.id)) \
        .join(post_tags) \
        .group_by(Tag.id) \
        .order_by(db.func.count(Tag.id).desc()) \
        .all()

    sidebar['top_tags'] = top_tags

    monthly_archives = Post.query \
        .add_columns(db.func.extract('year', Post.created_timestamp),
                     db.func.extract('month', Post.created_timestamp)) \
        .group_by(db.func.extract('year', Post.created_timestamp),
                  db.func.extract('month', Post.created_timestamp)) \
        .all()

    sidebar['monthly_archives'] = monthly_archives

    return sidebar


@page.route('/', methods=['GET', 'POST'])
@page.route('/index', methods=['GET', 'POST'])
@page.route('/index/<int:page_num>', methods=['GET', 'POST'])
def index(page_num=1):
    query = Post.query

    search = request.args.get('q')

    if search:
        query = query \
            .filter((Post.body.contains(search)) |
                    (Post.title.contains(search)))

    posts = query \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config.get('RABIANG_POSTS_PER_PAGE'),
                  False)

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/index.html',
        posts=posts,
        sidebar=sidebar)


@page.route('/<slug>', methods=['GET', 'POST'])
def detail_slug(slug):
    post = Post.query \
        .filter(Post.slug == slug) \
        .first_or_404()

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment()

        comment.name = form.name.data
        comment.email = form.email.data
        comment.body = form.body.data
        comment.ip_address = request.remote_addr
        comment.post_id = post.id

        db.session.add(comment)
        db.session.commit()

        flash(gettext('Your comment has been published.'))
        return redirect(url_for('page.detail_slug', slug=post.slug))

    comments = post.comments \
        .order_by(Comment.created_timestamp.asc()) \
        .all()

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/detail.html',
        post=post,
        form=form,
        comments=comments,
        sidebar=sidebar)


@page.route('/<int:post_id>', methods=['GET', 'POST'])
def detail_post_id(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment()

        comment.name = form.name.data
        comment.email = form.email.data
        comment.body = form.body.data
        comment.ip_address = request.remote_addr
        comment.post_id = post.id

        db.session.add(comment)
        db.session.commit()

        flash(gettext('Your comment has been published.'))
        return redirect(url_for('page.detail_slug', slug=post.slug))

    comments = post.comments \
        .order_by(Comment.created_timestamp.asc()) \
        .all()

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/detail.html',
        post=post,
        form=form,
        comments=comments,
        sidebar=sidebar)


@page.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        post = Post()

        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.status = form.status.data
        post.tags = form.tags.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You wrote a new post.'), 'success')
        return redirect(url_for('page.detail_slug', slug=post.slug))

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/create.html',
        form=form,
        sidebar=sidebar)


@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.status = form.status.data
        post.tags = form.tags.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You edited your post.'), 'success')
        return redirect(url_for('page.detail_slug', slug=post.slug))

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/edit.html',
        form=form,
        post_id=post_id,
        sidebar=sidebar)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

        flash(gettext('You deleted your post.'), 'success')
        return redirect(url_for('page.index'))

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/delete.html',
        form=form,
        post=post,
        sidebar=sidebar)


@page.route('/user/<username>', methods=['GET', 'POST'])
@page.route('/user/<username>/<int:page_num>', methods=['GET', 'POST'])
def user_index(username, page_num=1):
    author = User.query \
        .filter(User.username == username) \
        .first_or_404()

    posts = author.posts \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config.get('RABIANG_POSTS_PER_PAGE'),
                  False)

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/user.html',
        posts=posts,
        sidebar=sidebar)


@page.route('/tag', methods=['GET', 'POST'])
def tag_index():
    tags = Tag.query \
        .add_columns(db.func.count(Tag.id)) \
        .join(post_tags) \
        .group_by(Tag.id) \
        .order_by(Tag.name) \
        .all()

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/tag.html',
        tags=tags,
        sidebar=sidebar)


@page.route('/tag/<name>', methods=['GET', 'POST'])
@page.route('/tag/<name>/<int:page_num>', methods=['GET', 'POST'])
def tag_name(name, page_num=1):
    tag = Tag.query \
        .filter(Tag.name == name) \
        .first_or_404()

    posts = tag.posts \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config.get('RABIANG_POSTS_PER_PAGE'),
                  False)

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/tag_name.html',
        posts=posts,
        sidebar=sidebar)


@page.route('/month/<int:year>/<int:month>', methods=['GET', 'POST'])
@page.route('/month/<int:year>/<int:month>/<int:page_num>',
            methods=['GET', 'POST'])
def month_index(year, month, page_num=1):
    posts = Post.query \
        .filter((db.func.extract('year', Post.created_timestamp) == year) &
                (db.func.extract('month', Post.created_timestamp) == month)) \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config.get('RABIANG_POSTS_PER_PAGE'),
                  False)

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/user.html',
        posts=posts,
        sidebar=sidebar)
