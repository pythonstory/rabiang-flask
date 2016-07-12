# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Blueprint, render_template, current_app
from flask_babel import gettext, format_datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/admin/index.html')
