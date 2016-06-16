# -*- coding: utf-8 -*-

from flask import render_template

from . import forum


@forum.route('/')
def index():
    return render_template('default/forum/index.html')
