from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from .models import Module


class PageShowView(View):
    def get(self, request, *args, **kwargs):
        module = get_object_or_404(Module, slug=kwargs['slug'])

        theme = module.theme

        menu = theme.menu.all()

        try:
            # constraint: page has one document.
            document = module.documents.all()[0]
        except IndexError:
            return HttpResponseNotFound('<h1>Document does not exist.</h1>')

        context = {'theme': theme, 'menu': menu,
                   'document': document}
        return render(request, 'default/page/show.html', context)


class BlogShowView(View):
    def get(self, request, *args, **kwargs):
        module = get_object_or_404(Module, created__year=kwargs['year'],
                                   created__month=kwargs['month'],
                                   created__day=kwargs['day'],
                                   slug=kwargs['slug'])

        theme = module.theme

        menu = theme.menu.all()

        try:
            # constraint: blog has one document.
            document = module.documents.all()[0]
        except IndexError:
            return HttpResponseNotFound('<h1>Document does not exist.</h1>')

        context = {'theme': theme, 'menu': menu,
                   'document': document}
        return render(request, 'default/blog/show.html', context)


class BlogListView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('blog list')


class BlogArchiveView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here.

        return HttpResponse(
            'blog archive {} {}'.format(kwargs['year'], kwargs['month']))


class BoardListView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board list')


class BoardShowView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board show')


class BoardCreateView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board create')


class BoardEditView(View):
    def get(self, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board edit')


class BoardSaveView(View):
    def get(selfself, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board save')


class BoardUpdateView(View):
    def get(selfself, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board update')


class BoardDeleteView(View):
    def get(selfself, request, *args, **kwargs):
        # Business logic goes here.
        return HttpResponse('board delete')
