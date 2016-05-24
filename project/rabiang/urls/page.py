from django.conf.urls import include, url
from .. import views

urlpatterns = [
    # ex) /www/page/what-is-this
    url(r'^(?P<slug>[-\w]+)/$', views.PageShowView.as_view(), name='page_show'),
]
