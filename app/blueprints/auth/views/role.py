# -*- coding: utf-8 -*-
from flask import url_for, render_template, current_app
from flask_babel import gettext
from flask_login import login_required

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.models import User, Role
from app.blueprints.auth.views import auth


@auth.route('/role', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'manage')
def role_index():
    roles = Role.query \
        .order_by(Role.name.asc()) \
        .all()

    title = gettext('Role') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Role'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/role_index.html',
        roles=roles,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/role/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'manage')
def role_user_index(user_id):
    user = User.query.get_or_404(user_id)

    title = gettext('Role') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Role'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/role_user_index.html',
        role=user.role,
        title=title,
        breadcrumbs=breadcrumbs)
