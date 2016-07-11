# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, \
    current_app
from flask_babel import gettext
from flask_login import login_user

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.forms import LoginForm
from app.blueprints.auth.models import User
from app.blueprints.auth.views import auth


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
