# -*- coding: utf-8 -*-
from flask import redirect, url_for, flash
from flask_babel import gettext
from flask_login import logout_user, login_required

from app.blueprints.auth.decorators import permission_required
from app.blueprints.auth.views import auth


@auth.route('/logout', methods=['GET'])
@login_required
@permission_required('auth', 'authenticated')
def logout():
    logout_user()

    flash(gettext('You have been logged out'), 'success')

    return redirect(url_for('main.index'))
