# -*- coding: utf-8 -*-
from flask import Blueprint

page = Blueprint('page', __name__, url_prefix='/page')

from app.blueprints.page.views.post import post_index, post_detail_slug, \
    post_detail_id, post_create, post_edit, post_delete, post_recent_feed, \
    post_month_index, post_user_index
from app.blueprints.page.views.sidebar import sidebar_data
from app.blueprints.page.views.tag import tag_index, tag_detail
from app.blueprints.page.views.category import category_index, \
    category_detail, category_create, category_edit, category_delete
