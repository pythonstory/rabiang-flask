# -*- coding: utf-8 -*-

from datetime import datetime

from app import db


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)

    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Module: %s>' % self.title
