# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, current_app

forum = Blueprint('forum', __name__, url_prefix='/forum')


@forum.route('/')
def index():
    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/forum/index.html')
