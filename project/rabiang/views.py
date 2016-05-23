from django.http.response import HttpResponse, HttpResponseNotFound

from .models import Site

def page_show(request, site, slug):
    # site & theme
    try:
        site = Site.objects.get(name=site)
    except Site.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # module

    # layout

    # menu

    # breadcrumb

    # content

    return HttpResponse(
        'page show {} {} {}'.format(site, site.theme.name, slug))


def blog_show(request, site, year, month, day, slug):
    return HttpResponse(
        'blog show {} {} {} {} {}'.format(site, year, month, day, slug))


def blog_list(request, site):
    return HttpResponse('blog list {}'.format(site))


def blog_archive(request, site, year, month):
    return HttpResponse(
        'blog archive {} {} {}'.format(site, year, month))


def board_list(request, site):
    return HttpResponse('board list {}'.format(site))


def board_show(request, site):
    return HttpResponse('board show {}'.format(site))


def board_create(request, site):
    return HttpResponse('board create {}'.format(site))


def board_edit(request, site):
    return HttpResponse('board edit {}'.format(site))


def board_save(request, site):
    return HttpResponse('board save {}'.format(site))


def board_update(request, site):
    return HttpResponse('board update {}'.format(site))


def board_delete(request, site):
    return HttpResponse('board delete {}'.format(site))
