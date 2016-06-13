# -*- coding: utf-8 -*-
from flask import Blueprint

page = Blueprint('page', __name__)

from . import views, errors
