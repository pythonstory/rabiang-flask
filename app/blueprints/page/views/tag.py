# -*- coding: utf-8 -*-

from flask import render_template, url_for, \
    current_app
from flask_babel import gettext

from app.blueprints.auth.decorators import permission_required
from app.blueprints.page.models import Post, Tag, post_tag
from app.blueprints.page.views import page
from app.blueprints.page.views.sidebar import sidebar_data
from app.extensions import db


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
