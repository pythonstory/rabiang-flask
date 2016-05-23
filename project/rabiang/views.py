from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Module


def page_show(request, slug):
    module = get_object_or_404(Module, slug=slug)

    site = module.site
    theme = module.theme
    layout = module.layout

    menu = layout.menu
    documents = module.documents

    context = {'site': site, 'theme': theme, 'layout': layout, 'menu': menu,
               'documents': documents}
    return render(request, 'default/page/show.html', context)


def blog_show(request, year, month, day, slug):
    return HttpResponse(
        'blog show {} {} {} {}'.format(year, month, day, slug))


def blog_list(request):
    return HttpResponse('blog list')


def blog_archive(request, year, month):
    return HttpResponse(
        'blog archive {} {}'.format(year, month))


def board_list(request):
    return HttpResponse('board list {}')


def board_show(request):
    return HttpResponse('board show {}')


def board_create(request):
    return HttpResponse('board create {}')


def board_edit(request):
    return HttpResponse('board edit {}')


def board_save(request):
    return HttpResponse('board save {}')


def board_update(request):
    return HttpResponse('board update {}')


def board_delete(request):
    return HttpResponse('board delete {}')
