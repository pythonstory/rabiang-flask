from django.conf.urls import include, url
from .. import views

urlpatterns = [
    # ex) /www/page/what-is-this
    url(r'^(?P<slug>\w+)/$', views.page_show, name='page_show'),
]
