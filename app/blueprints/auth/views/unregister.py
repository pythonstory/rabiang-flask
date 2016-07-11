# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, flash, current_app
from flask_babel import gettext
from flask_login import login_required, current_user

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.forms import UnregisterForm
from app.blueprints.auth.models import User
from app.blueprints.auth.views import auth
from app.blueprints.page.models import Post
from app.extensions import db


@auth.route('/unregister', methods=['GET', 'POST'])
@login_required
@permission_required('auth', 'authenticated')
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
