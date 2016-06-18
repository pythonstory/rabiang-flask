# -*- coding: utf-8 -*-
from datetime import datetime

from flask import url_for

from app import db
from app.utils.html import slugify


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)

    body = db.Column(db.Text)

    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def generate_slug(self):
        self.slug = slugify(self.title)

    def get_slug_url(self):
        return url_for('page.detail_slug', slug=self.slug)

    def get_permanent_url(self):
        return url_for('page.detail_post_id', post_id=self.id)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post: %s>' % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.Text)

    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='comments')

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comment: %s>' % self.body
