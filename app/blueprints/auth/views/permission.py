# -*- coding: utf-8 -*-
from flask import url_for, render_template, current_app
from flask_babel import gettext
from flask_login import login_required

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.models import RolePermissionResource, Permission, \
    Resource, Role
from app.blueprints.auth.views import auth


@auth.route('/permission', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'manage')
def permission_index():
    permissions = Permission.query \
        .join(Resource) \
        .join(RolePermissionResource) \
        .order_by(Resource.name.asc(), Permission.bit.asc()) \
        .all()

    title = gettext('Permission') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Permission'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] +
        '/auth/permission_index.html',
        permissions=permissions,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/permission/resource/<resource_name>', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'manage')
def permission_resource(resource_name):
    permissions = Permission.query \
        .join(Resource) \
        .join(RolePermissionResource) \
        .filter(Resource.name == resource_name) \
        .order_by(Resource.name.asc(), Permission.bit.asc()) \
        .all()

    title = gettext('Permission') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Permission'),
        'href': url_for('auth.permission_index'),
    }, {
        'text': '{} - {}'.format(gettext('Resource'), resource_name),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] +
        '/auth/permission_resource.html',
        permissions=permissions,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/permission/role/<int:role_id>', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'manage')
def permission_role(role_id):
    role = Role.query.get_or_404(role_id)

    permissions = Permission.query \
        .join(Resource) \
        .join(RolePermissionResource) \
        .filter((RolePermissionResource.role_id == role_id) &
                (RolePermissionResource.permission.op('&')(Permission.bit))) \
        .all()

    title = gettext('Permission') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Permission'),
        'href': url_for('auth.permission_index'),
    }, {
        'text': '{} - {}'.format(gettext('Role'), role.name),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] +
        '/auth/permission_role.html',
        permissions=permissions,
        title=title,
        breadcrumbs=breadcrumbs)
