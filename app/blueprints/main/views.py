# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Blueprint, render_template, current_app
from flask_babel import gettext, format_datetime

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def index():
    print(format_datetime(datetime(1987, 3, 5, 17, 12)))
    print(gettext('Home'))

    title = current_app.config['RABIANG_SITE_NAME']

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/main/index.html',
        title=title)
