# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, current_app
from flask_babel import gettext, format_datetime

from . import main


@main.route('/')
def index():
    print(format_datetime(datetime(1987, 3, 5, 17, 12)))
    print(gettext('Home'))
    current_app.logger.info('Information: 3 + 2 = %d', 5)
    return render_template('default/main/index.html')
