# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, flash, current_app
from flask_babel import gettext

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.forms import RegisterForm
from app.blueprints.auth.models import User, Role
from app.blueprints.auth.views import auth
from app.extensions import db


@auth.route('/register', methods=['GET', 'POST'])
@permission_required('auth', 'register')
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User()

        role = Role.query \
            .filter(Role.name == 'User') \
            .first()

        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.role = role
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
