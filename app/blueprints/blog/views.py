# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, current_app
from flask_babel import gettext, format_datetime

from . import blog


@blog.route('/')
def index():
    return render_template('default/blog/index.html')
