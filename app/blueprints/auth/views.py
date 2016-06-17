# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, render_template, flash
from flask_babel import gettext
from flask_login import login_user, logout_user, login_required

from . import auth
from .forms import LoginForm
from .models import User


@auth.route('/')
def index():
    return render_template('default/auth/index.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            flash(gettext('You successfully logged in'), 'success')

            return redirect(request.args.get('next') or url_for('main.index'))

        flash(gettext('Invalid username or password'), 'success')

    return render_template('default/auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    flash(gettext('You have been logged out'), 'success')

    return redirect(url_for('main.index'))


@auth.route('/register')
def register():
    return "register"


@auth.route('/unregister')
@login_required
def unregister():
    return "unregister"
