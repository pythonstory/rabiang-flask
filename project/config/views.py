from django.shortcuts import render

def default_index(request):
    return render(request, 'default/main/index.html')