# -*- coding: utf-8 -*-

from flask import render_template

from . import auth


@auth.route('/')
def index():
    return render_template('default/auth/index.html')


@auth.route('/login')
def login():
    return render_template('default/auth/login.html')


@auth.route('/logout')
def logout():
    return "logout"


@auth.route('/register')
def register():
    return "register"


@auth.route('/unregister')
def unregister():
    return "unregister"
