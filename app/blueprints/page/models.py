# -*- coding: utf-8 -*-

from datetime import datetime

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)

    body = db.Column(db.Text)

    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

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
