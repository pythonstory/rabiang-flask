# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, url_for, render_template, \
    flash, current_app
from flask_babel import gettext
from flask_login import login_user, logout_user, login_required, current_user

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.forms import LoginForm, RegisterForm, UnregisterForm, \
    ChangePasswordForm
from app.blueprints.auth.models import User, RolePermissionResource, \
    Permission, Resource, Role
from app.blueprints.page.models import Post
from app.extensions import db

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
@permission_required('auth', 'login')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query \
            .filter(User.email == form.email.data) \
            .first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            flash(gettext('You successfully logged in'), 'success')
            return redirect(request.args.get('next') or url_for('main.index'))

        flash(gettext('Invalid username or password'), 'success')

    title = gettext('Login') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Login'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/login.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/logout', methods=['GET'])
@login_required
@permission_required('auth', 'logout')
def logout():
    logout_user()

    flash(gettext('You have been logged out'), 'success')

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
@permission_required('auth', 'register')
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User()

        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.active = True

        db.session.add(user)
        db.session.commit()

        flash(gettext('You can now login.'), 'success')
        return redirect(url_for('auth.login'))

    title = gettext('Sign up') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Sign up'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/register.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/unregister', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'login')
def unregister():
    user = User.query.get(current_user.id)

    form = UnregisterForm()

    if form.validate_on_submit():
        Post.query \
            .filter(Post.author_id == current_user.id) \
            .update({'status': Post.STATUS_DELETED})

        db.session.delete(user)
        db.session.commit()

        flash(gettext('Your account was deleted.'), 'success')
        return redirect(url_for('page.post_index'))

    title = gettext('Delete account') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Delete account'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/unregister.html',
        form=form,
        user=user,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'login')
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)

        if user is not None and user.verify_password(form.old_password.data):
            user.password = form.password.data

            db.session.add(user)
            db.session.commit()

            flash(gettext('You changed your password.'), 'success')
            return redirect(url_for('page.post_index'))

        flash(gettext('Old password is wrong.'), 'danger')
        return redirect(url_for('auth.change_password'))

    title = gettext('Change password') + ' - ' + \
        current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Change password'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/auth/change_password.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs)


@auth.route('/reset-password', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'login')
def reset_password():
    return 'reset password'


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
