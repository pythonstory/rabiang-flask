"""Rabiang project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default_index, name='default_index'),
    url(r'^page/', include('rabiang.urls.page', namespace='page', app_name='page')),
    url(r'^board/', include('rabiang.urls.board', namespace='board', app_name='board')),
    url(r'^blog/', include('rabiang.urls.blog', namespace='blog', app_name='blog')),
    url(r'^admin/', admin.site.urls),
]
