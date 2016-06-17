# -*- coding: utf-8 -*-

from datetime import datetime

from flask_login import UserMixin

from app import db
from app import login_manager
from app.utils.html import slugify


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))

    slug = db.Column(db.String(100), unique=True)

    active = db.Column(db.Boolean, default=True)

    created_timestamp = db.Column(db.DateTime, default=datetime.now)

    def generate_slug(self):
        self.slug = slugify(self.username)

    def verify_password(self, password):
        return True

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User: %s>' % self.username


@login_manager.user_loader
def _user_loader(user_id):
    # User loader callback function
    return User.query.get(int(user_id))
