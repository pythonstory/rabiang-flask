# -*- coding: utf-8 -*-
from flask import Blueprint

forum = Blueprint('forum', __name__)

from . import views, models
