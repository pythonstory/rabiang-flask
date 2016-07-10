# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from flask import render_template, request, redirect, url_for, \
    flash, current_app
from flask_babel import gettext
from flask_login import login_required, current_user
from werkzeug.contrib.atom import AtomFeed

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.models import User
from app.blueprints.page.forms import PostForm, CommentForm, DeletePostForm
from app.blueprints.page.models import Post, Comment, PageCategory
from app.blueprints.page.views import page
from app.blueprints.page.views.sidebar import sidebar_data
from app.extensions import db
from app.utils.structure import build_tree_tuple_list


@page.route('/', methods=['GET', 'POST'])
@page.route('/index', methods=['GET', 'POST'])
@page.route('/index/<int:page_num>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_index(page_num=1):
    query = Post.query

    search = request.args.get('q')

    if search:
        query = query \
            .filter((Post.body.contains(search)) |
                    (Post.title.contains(search)))

    posts = query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config['RABIANG_POSTS_PER_PAGE'],
                  False)

    title = gettext('Blog') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_index.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/<slug>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_detail_slug(slug):
    post = Post.query \
        .filter(Post.slug == slug) \
        .first_or_404()

    if post.status != Post.STATUS_PUBLIC \
            and (not current_user.is_authenticated
                 or current_user.id != post.author_id):
        return render_template(current_app.config['RABIANG_SITE_THEME'] +
                               '/404.html'), 404

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

        flash(gettext('Your comment has been published.'), 'success')
        return redirect(url_for('page.post_detail_slug', slug=post.slug))

    comments = post.comments \
        .order_by(Comment.created_timestamp.asc()) \
        .all()

    title = post.title + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': post.title,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_detail.html',
        post=post,
        Post=Post,
        form=form,
        comments=comments,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/<int:post_id>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_detail_id(post_id):
    post = Post.query.get_or_404(post_id)

    if post.status != Post.STATUS_PUBLIC \
            and (not current_user.is_authenticated
                 or current_user.id != post.author_id):
        return render_template(current_app.config['RABIANG_SITE_THEME'] +
                               '/404.html'), 404

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

        flash(gettext('Your comment has been published.'), 'success')
        return redirect(url_for('page.post_detail_slug', slug=post.slug))

    comments = post.comments \
        .order_by(Comment.created_timestamp.asc()) \
        .all()

    title = post.title + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': post.title,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_detail.html',
        post=post,
        Post=Post,
        form=form,
        comments=comments,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def post_create():
    form = PostForm()

    form.category.choices = build_tree_tuple_list(PageCategory, prefix=True)

    if form.validate_on_submit():
        post = Post()

        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.status = form.status.data
        post.format = current_app.config['RABIANG_POST_HTML_FORMAT']
        post.category_id = form.category.data
        post.tags = form.tags.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You wrote a new post.'), 'success')
        return redirect(url_for('page.post_detail_slug', slug=post.slug))

    title = gettext('Write a new post') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Write a new post'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_create.html',
        form=form,
        Post=Post,
        title=title,
        breadcrumbs=breadcrumbs)


@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'edit')
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)

    if not current_user.is_authenticated or current_user.id != post.author_id:
        return render_template(current_app.config['RABIANG_SITE_THEME'] +
                               '/404.html'), 404

    form = PostForm(obj=post)

    form.category.choices = build_tree_tuple_list(PageCategory, prefix=True)

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.status = form.status.data
        post.format = current_app.config['RABIANG_POST_HTML_FORMAT']
        post.category_id = form.category.data
        post.tags = form.tags.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You edited your post.'), 'success')
        return redirect(url_for('page.post_detail_slug', slug=post.slug))

    # Set default category option when written
    form.category.data = post.category_id if post.category_id else 0

    title = gettext('Edit') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': '{} - {}'.format(gettext('Edit'), post.title),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_edit.html',
        form=form,
        post=post,
        Post=Post,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'delete')
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)

    if not current_user.is_authenticated or current_user.id != post.author_id:
        return render_template(current_app.config['RABIANG_SITE_THEME'] +
                               '/404.html'), 404

    form = DeletePostForm()

    if form.validate_on_submit():
        post.status = Post.STATUS_DELETED

        db.session.add(post)
        db.session.commit()

        flash(gettext('You deleted your post.'), 'success')
        return redirect(url_for('page.post_index'))

    title = gettext('Delete') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': '{} - {}'.format(gettext('Delete'), post.title),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_delete.html',
        form=form,
        post=post,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/feed', methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_recent_feed():
    feed = AtomFeed(
        gettext('Latest Blog Posts'),
        feed_url=request.url,
        url=request.url_root,
        author=request.url_root
    )

    posts = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Post.created_timestamp.desc()) \
        .limit(current_app.config['RABIANG_RECENT_POSTS_FOR_FEED']) \
        .all()

    for post in posts:
        feed.add(
            post.title,
            post.body,
            content_type='html',
            url=urljoin(request.url_root,
                        url_for("page.post_detail_slug", slug=post.slug)),
            updated=post.modified_timestamp,
            published=post.created_timestamp
        )

    return feed.get_response()


@page.route('/user/<username>', methods=['GET', 'POST'])
@page.route('/user/<username>/<int:page_num>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_user_index(username, page_num=1):
    author = User.query \
        .filter(User.username == username) \
        .first_or_404()

    query = author.posts

    if current_user.is_authenticated and current_user.id == author.id:
        query = query.filter((Post.status == Post.STATUS_PUBLIC) |
                             (Post.status == Post.STATUS_DRAFT))
    else:
        query = query.filter(Post.status == Post.STATUS_PUBLIC)

    posts = query \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config['RABIANG_POSTS_PER_PAGE'],
                  False)

    title = username + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': username,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/post_user_index.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/month/<int:year>/<int:month>', methods=['GET', 'POST'])
@page.route('/month/<int:year>/<int:month>/<int:page_num>',
            methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_month_index(year, month, page_num=1):
    posts = Post.query \
        .filter((db.func.extract('year', Post.created_timestamp) == year) &
                (db.func.extract('month', Post.created_timestamp) == month)) \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config['RABIANG_POSTS_PER_PAGE'],
                  False)

    title = gettext('Blog Archives') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Blog Archives'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config[
            'RABIANG_SITE_THEME'] + '/page/post_month_index.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)
