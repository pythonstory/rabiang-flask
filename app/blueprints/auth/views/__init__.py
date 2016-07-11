# -*- coding: utf-8 -*-
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

from app.blueprints.auth.views.login import login
from app.blueprints.auth.views.logout import logout
from app.blueprints.auth.views.register import register
from app.blueprints.auth.views.unregister import unregister
from app.blueprints.auth.views.profile import change_password, reset_password
from app.blueprints.auth.views.role import role_index, role_user_index
from app.blueprints.auth.views.permission import permission_index, \
    permission_resource, permission_role
from app.blueprints.auth.views.resource import resource_index
