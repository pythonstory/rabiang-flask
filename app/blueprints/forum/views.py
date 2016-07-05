# -*- coding: utf-8 -*-
from flask import render_template, current_app

from app.blueprints.forum import forum


@forum.route('/')
def index():
    return render_template(
        current_app.config.get('RABIANG_SITE_THEME') + '/forum/index.html')
