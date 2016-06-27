# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from flask import render_template, request, redirect, url_for, flash, \
    current_app
from flask_babel import gettext
from flask_login import login_required, current_user
from werkzeug.contrib.atom import AtomFeed

from app import db
from app.blueprints.auth.models import User
from . import page
from .forms import PostForm, CommentForm, DeletePostForm
from .models import Post, Comment, Tag, post_tag


def sidebar_data():
    sidebar = {}

    recent_posts = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Post.created_timestamp.desc()) \
        .limit(current_app.config.get('RABIANG_RECENT_POSTS')) \
        .all()

    sidebar['recent_posts'] = recent_posts

    recent_comments = Comment.query \
        .join(Post) \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Comment.created_timestamp.desc()) \
        .limit(current_app.config.get('RABIANG_RECENT_COMMENTS')) \
        .all()

    sidebar['recent_comments'] = recent_comments

    top_tags = Tag.query \
        .add_columns(db.func.count(Tag.id)) \
        .join(post_tag) \
        .join(Post) \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .group_by(Tag.id) \
        .order_by(db.func.count(Tag.id).desc()) \
        .all()

    sidebar['top_tags'] = top_tags

    monthly_archives = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
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
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config.get('RABIANG_POSTS_PER_PAGE'),
                  False)

    title = gettext('Blog') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/index.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/feed', methods=['GET', 'POST'])
def recent_feed():
    feed = AtomFeed(
        gettext('Latest Blog Posts'),
        feed_url=request.url,
        url=request.url_root,
        author=request.url_root
    )

    posts = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Post.created_timestamp.desc()) \
        .limit(current_app.config.get('RABIANG_RECENT_POSTS_FOR_FEED')) \
        .all()

    for post in posts:
        feed.add(
            post.title,
            post.body,
            content_type='html',
            url=urljoin(request.url_root,
                        url_for("page.detail_slug", slug=post.slug)),
            updated=post.modified_timestamp,
            published=post.created_timestamp
        )

    return feed.get_response()


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

    title = post.title + ' - ' + current_app.config.get('RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': post.title,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/detail.html',
        post=post,
        form=form,
        comments=comments,
        title=title,
        breadcrumbs=breadcrumbs,
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

    title = post.title + ' - ' + current_app.config.get('RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': post.title,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/detail.html',
        post=post,
        form=form,
        comments=comments,
        title=title,
        breadcrumbs=breadcrumbs,
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

    title = gettext('Write a new post') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': gettext('Write a new post'),
        'href': False,
    }]

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/create.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


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

    title = gettext('Edit') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': gettext('Edit'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/edit.html',
        form=form,
        post_id=post_id,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    form = DeletePostForm()

    if form.validate_on_submit():
        post.status = Post.STATUS_DELETED

        db.session.add(post)
        db.session.commit()

        flash(gettext('You deleted your post.'), 'success')
        return redirect(url_for('page.index'))

    title = gettext('Delete') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': gettext('Delete'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/delete.html',
        form=form,
        post=post,
        title=title,
        breadcrumbs=breadcrumbs,
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

    title = username + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': username,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/user.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/tag', methods=['GET', 'POST'])
def tag_index():
    tags = Tag.query \
        .add_columns(db.func.count(Tag.id)) \
        .join(post_tag) \
        .join(Post) \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .group_by(Tag.id) \
        .order_by(Tag.name) \
        .all()

    title = gettext('Tag') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': gettext('Tag'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/tag.html',
        tags=tags,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/tag/<tag_name>', methods=['GET', 'POST'])
@page.route('/tag/<tag_name>/<int:page_num>', methods=['GET', 'POST'])
def tag_name(tag_name, page_num=1):
    tag = Tag.query \
        .filter(Tag.name == tag_name) \
        .first_or_404()

    posts = tag.posts \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config.get('RABIANG_POSTS_PER_PAGE'),
                  False)

    title = gettext('Tag') + ' - ' + tag_name + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': gettext('Tag'),
        'href': url_for('page.tag_index'),
    }, {
        'text': tag_name,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/tag_name.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
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

    title = gettext('Blog Archives') + ' - ' + current_app.config.get(
        'RABIANG_SITE_NAME')

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.index'),
    }, {
        'text': gettext('Blog Archives'),
        'href': url_for('page.tag_index'),
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/page/user.html',
        posts=posts,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)
