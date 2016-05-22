from django.conf.urls import include, url
from .. import views

urlpatterns = [
    # ex) /www/board/list
    url(r'^list/$', views.board_list, name='board_list'),

    # ex) /www/board/show
    url(r'^show/$', views.board_show, name='board_show'),

    # ex) /www/board/create
    url(r'^create/$', views.board_create, name='board_create'),

    # ex) /www/board/edit
    url(r'^edit/$', views.board_edit, name='board_edit'),

    # ex) /www/board/save
    url(r'^save/$', views.board_save, name='board_save'),

    # ex) /www/board/update
    url(r'^update/$', views.board_update, name='board_update'),

    # ex) /www/board/delete
    url(r'^delete/$', views.board_delete, name='board_delete'),
]
