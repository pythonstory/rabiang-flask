# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager


class Base(db.Model):
    __abstract__ = True

    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now,
                                   onupdate=datetime.now)


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        # password field is hidden and not added even on the table.
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User: %r>' % self.username


@login_manager.user_loader
def _user_loader(user_id):
    # User loader callback function
    return User.query.get(int(user_id))
