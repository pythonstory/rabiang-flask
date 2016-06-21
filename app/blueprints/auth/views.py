# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash
from flask_babel import gettext
from flask_login import login_user, logout_user, login_required

from app import db
from . import auth
from .forms import LoginForm, RegisterForm
from .models import User


@auth.route('/')
def index():
    return render_template('default/auth/index.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query \
            .filter_by(email=form.email.data) \
            .first()

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


@auth.route('/register', methods=['GET', 'POST'])
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

    return render_template('default/auth/register.html', form=form)


@auth.route('/unregister', methods=['GET', 'POST'])
@login_required
def unregister():
    return 'unregister'


@auth.route('/change-password')
@login_required
def change_password():
    return 'change password'


@auth.route('/reset-password')
def reset_password():
    return 'reset password'
