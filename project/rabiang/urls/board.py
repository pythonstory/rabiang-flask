from django.conf.urls import include, url
from .. import views

urlpatterns = [
    # ex) /www/board/list
    url(r'^list/$', views.BoardListView.as_view(), name='board_list'),

    # ex) /www/board/show
    url(r'^show/$', views.BoardShowView.as_view(), name='board_show'),

    # ex) /www/board/create
    url(r'^create/$', views.BoardCreateView.as_view(), name='board_create'),

    # ex) /www/board/edit
    url(r'^edit/$', views.BoardEditView.as_view(), name='board_edit'),

    # ex) /www/board/save
    url(r'^save/$', views.BoardSaveView.as_view(), name='board_save'),

    # ex) /www/board/update
    url(r'^update/$', views.BoardUpdateView.as_view(), name='board_update'),

    # ex) /www/board/delete
    url(r'^delete/$', views.BoardDeleteView.as_view(), name='board_delete'),
]
