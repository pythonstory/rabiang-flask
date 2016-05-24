from django.conf.urls import include, url
from .. import views

urlpatterns = [
    # ex) /www/blog/2016-05-23/what-is-this
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.BlogShowView.as_view(), name='blog_show'),

    # ex) /www/blog/list
    url(r'^list/$',
        views.BlogListView.as_view(), name='blog_list'),

    # ex) /www/blog/archive/2016/05/
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.BlogArchiveView.as_view(), name='blog_archive'),

]

"""
/www/account/login
/www/account/login-proc
/www/account/logout
/www/account/logout-proc
/www/account/signup
/www/account/edit-profile
/www/account/save
/www/account/delete
"""
