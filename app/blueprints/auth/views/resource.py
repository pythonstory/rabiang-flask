# -*- coding: utf-8 -*-
from flask import url_for, render_template, current_app
from flask_babel import gettext
from flask_login import login_required

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.models import Resource
from app.blueprints.auth.views import auth


@auth.route('/resource', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'manage')
def resource_index():
    resources = Resource.query \
        .all()

    title = gettext('Resource') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Resource'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/resource_index.html',
        resources=resources,
        title=title,
        breadcrumbs=breadcrumbs)
