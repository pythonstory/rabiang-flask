# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, flash, current_app
from flask_babel import gettext
from flask_login import login_required, current_user

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.forms import ChangePasswordForm
from app.blueprints.auth.models import User
from app.blueprints.auth.views import auth
from app.extensions import db


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'authenticated')
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
@permission_required('auth', 'authenticated')
def reset_password():
    return 'reset password'
