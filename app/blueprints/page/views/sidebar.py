# -*- coding: utf-8 -*-
from flask import current_app

from app.blueprints.page.models import Post, Comment, Tag, post_tag, \
    PageCategory
from app.extensions import db
from app.utils.structure import build_tree_dictionary


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
