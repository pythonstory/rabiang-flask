# -*- coding: utf-8 -*-
from datetime import datetime

from flask import url_for

from app import db

post_tag = db.Table('post_tag',
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Post(db.Model):
    __tablename__ = 'post'

    STATUS_DRAFT = 0
    STATUS_PUBLIC = 1
    STATUS_PRIVATE = 2
    STATUS_DELETED = 3

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_DRAFT)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now,
                                   onupdate=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
                             backref=db.backref('posts', lazy='dynamic'))

    tags = db.relationship('Tag', secondary=post_tag,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    def get_slug_url(self):
        return url_for('page.detail_slug', slug=self.slug)

    def get_permanent_url(self):
        return url_for('page.detail_post_id', post_id=self.id)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post: %r>' % self.title


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    body = db.Column(db.Text)
    ip_address = db.Column(db.String(64))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now,
                                   onupdate=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post',
                           backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comment: %r>' % self.body


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag: %r>' % self.name
