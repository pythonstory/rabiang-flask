from django.shortcuts import render
from django.http.response import HttpResponse

def page_show(request, site, slug):
    return HttpResponse('page show' + site + slug)