from django.conf.urls import include, url
from . import views

urlpatterns = [
    """
    /www/page/slug
    /www/blog/slug
    /www/board/list
    /www/board/show
    /www/board/create
    /www/board/edit
    /www/board/save
    /www/board/update
    /www/board/delete
    /www/account/login
    /www/account/login-proc
    /www/account/logout
    /www/account/logout-proc
    /www/account/signup
    /www/account/edit-profile
    /www/account/save
    /www/account/delete
    """
]
