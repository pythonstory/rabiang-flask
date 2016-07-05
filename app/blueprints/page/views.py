# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, current_app
from flask_babel import gettext
from flask_login import login_required, current_user
from werkzeug.contrib.atom import AtomFeed

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.models import User
from app.blueprints.page.forms import PostForm, CommentForm, DeletePostForm, \
    CategoryForm, DeleteCategoryForm
from app.blueprints.page.models import Post, Comment, Tag, post_tag, \
    PageCategory
from app.extensions import db
from app.utils.structure import build_tree_dictionary, build_tree_tuple_list, \
    build_tree_list

page = Blueprint('page', __name__, url_prefix='/page')


def sidebar_data():
    sidebar = {}

    categories = build_tree_dictionary(PageCategory)

    sidebar['categories'] = categories

    recent_posts = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Post.created_timestamp.desc()) \
        .limit(current_app.config['RABIANG_RECENT_POSTS']) \
        .all()

    sidebar['recent_posts'] = recent_posts

    recent_comments = Comment.query \
        .join(Post) \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .order_by(Comment.created_timestamp.desc()) \
        .limit(current_app.config['RABIANG_RECENT_COMMENTS']) \
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
        current_app.config['RABIANG_SITE_THEME'] + '/page/index.html',
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
        current_app.config['RABIANG_SITE_THEME'] + '/page/detail.html',
        post=post,
        form=form,
        comments=comments,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/<int:post_id>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def post_detail_id(post_id):
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
        current_app.config['RABIANG_SITE_THEME'] + '/page/detail.html',
        post=post,
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
        current_app.config['RABIANG_SITE_THEME'] + '/page/create.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'edit')
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)

    categories = build_tree_tuple_list(PageCategory, prefix=True)

    form = PostForm(obj=post)

    form.category.choices = categories

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.body = form.body.data
        post.status = form.status.data
        post.category_id = form.category.data
        post.tags = form.tags.data
        post.author = current_user

        db.session.add(post)
        db.session.commit()

        flash(gettext('You edited your post.'), 'success')
        return redirect(url_for('page.post_detail_slug', slug=post.slug))

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
        current_app.config['RABIANG_SITE_THEME'] + '/page/edit.html',
        form=form,
        post_id=post_id,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'delete')
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)

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
        current_app.config['RABIANG_SITE_THEME'] + '/page/delete.html',
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

    posts = author.posts \
        .filter(Post.status == Post.STATUS_PUBLIC) \
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
        current_app.config['RABIANG_SITE_THEME'] + '/page/user.html',
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
        'href': url_for('page.tag_index'),
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/user.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/tag', methods=['GET', 'POST'])
@permission_required('post', 'view')
def tag_index():
    tags = Tag.query \
        .add_columns(db.func.count(Tag.id)) \
        .join(post_tag) \
        .join(Post) \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .group_by(Tag.id) \
        .order_by(Tag.name) \
        .all()

    title = gettext('Tag') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Tag'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/tag.html',
        tags=tags,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/tag/<tag_name>', methods=['GET', 'POST'])
@page.route('/tag/<tag_name>/<int:page_num>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def tag_detail(tag_name, page_num=1):
    tag = Tag.query \
        .filter(Tag.name == tag_name) \
        .first_or_404()

    posts = tag.posts \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num, current_app.config['RABIANG_POSTS_PER_PAGE'],
                  False)

    title = gettext('Tag') + ' - ' + tag_name + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Tag'),
        'href': url_for('page.tag_index'),
    }, {
        'text': tag_name,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/tag_name.html',
        posts=posts,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/category', methods=['GET', 'POST'])
@permission_required('post', 'create')
def category_index():
    categories = build_tree_dictionary(PageCategory)

    title = gettext('Category') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Category'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category.html',
        categories=categories,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/category/<category_name>', methods=['GET', 'POST'])
@page.route('/category/<category_name>/<int:page_num>', methods=['GET', 'POST'])
@permission_required('post', 'create')
def category_detail(category_name, page_num=1):
    category = PageCategory.query \
        .filter(PageCategory.name == category_name) \
        .first_or_404()

    categories = build_tree_list(PageCategory, category)

    # Lookup posts with specified category and its descendants.
    category_names = [category.name]
    category_names.extend([category.name for category in categories])

    posts = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .join(PageCategory) \
        .filter(PageCategory.name.in_(category_names)) \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num,
                  current_app.config['RABIANG_POSTS_PER_PAGE'],
                  False)

    title = gettext('Category') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Category'),
        'href': False,
    }, {
        'text': category_name,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_detail.html',
        title=title,
        posts=posts,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/category/create', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def category_create():
    form = CategoryForm()

    categories = build_tree_tuple_list(PageCategory, prefix=True)

    form.parent.choices = [(0, gettext('Root Category'))]
    form.parent.choices.extend(categories)

    if form.validate_on_submit():
        page_category = PageCategory()

        page_category.name = form.name.data
        page_category.order = form.order.data

        if form.parent.data == 0:
            page_category.parent_id = None
        else:
            page_category.parent_id = form.parent.data

        db.session.add(page_category)
        db.session.commit()

        flash(gettext('You added a new category.'), 'success')
        return redirect(url_for('page.category_create'))

    title = gettext('Add categories') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Add categories'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_create.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs,
        categories=categories
    )


@page.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def category_edit(category_id):
    page_category = PageCategory.query.get_or_404(category_id)

    categories = build_tree_tuple_list(PageCategory, prefix=True)

    form = CategoryForm(obj=page_category)

    form.parent.choices = [(0, gettext('Root Category'))]
    form.parent.choices.extend(categories)

    if form.validate_on_submit():
        if form.parent.data != page_category.id:
            page_category.name = form.name.data
            page_category.order = form.order.data

            if form.parent.data == 0:
                page_category.parent_id = None
            else:
                page_category.parent_id = form.parent.data

            db.session.add(page_category)
            db.session.commit()

        flash(gettext('You updated the category.'), 'success')
        return redirect(url_for('page.category_edit', category_id=category_id))

    form.parent.data = page_category.parent_id if page_category.parent_id else 0

    title = gettext('Edit categories') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': '{} - {}'.format(gettext('Edit categories'),
                                 page_category.name),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_edit.html',
        form=form,
        category_id=category_id,
        title=title,
        breadcrumbs=breadcrumbs,
        categories=categories
    )


@page.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def category_delete(category_id):
    page_category = PageCategory.query.get_or_404(category_id)

    form = DeleteCategoryForm()

    if form.validate_on_submit():
        db.session.delete(page_category)
        db.session.commit()

        flash(gettext('You deleted the category.'), 'success')
        return redirect(url_for('page.category_create'))

    title = gettext('Delete') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': '{} - {}'.format(gettext('Delete a category'),
                                 page_category.name),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_delete.html',
        form=form,
        page_category=page_category,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)
