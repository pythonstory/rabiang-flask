# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app

from app.blueprints.auth.decorators import has_role

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET', 'POST'])
@has_role('Admin')
def index():
    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/admin/index.html')
