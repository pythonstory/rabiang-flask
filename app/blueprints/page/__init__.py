# -*- coding: utf-8 -*-
from flask import Blueprint

page = Blueprint('page', __name__, url_prefix='/page')

from app.blueprints.page import views, models
