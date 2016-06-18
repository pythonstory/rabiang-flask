# -*- coding: utf-8 -*-
from flask import Blueprint

page = Blueprint('page', __name__, url_prefix='/page')

from . import views, models
