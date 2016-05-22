from django.shortcuts import render
from django.http.response import HttpResponse

def default_index(request):
    return HttpResponse('Hello')