from django.http.response import HttpResponse
from django.views.generic import View, DetailView

from .models import Module


class PageShowView(DetailView):
    model = Module

    def get_queryset(self):
        qs = super(PageShowView, self).get_queryset()
        return qs.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PageShowView, self).get_context_data(**kwargs)
        context['page'] = self.object
        context['document'] = self.object.documents.all()[0]
        context['menu'] = self.object.theme.menu.all()
        return context

    def get_template_names(self):
        return self.object.theme.name + '/page/show.html'


class BlogShowView(DetailView):
    model = Module

    def get_queryset(self):
        qs = super(BlogShowView, self).get_queryset()

        return qs.filter(created__year=self.kwargs['year'],
                         created__month=self.kwargs['month'],
                         created__day=self.kwargs['day'],
                         slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(BlogShowView, self).get_context_data(**kwargs)
        context['blog'] = self.object
        context['document'] = self.object.documents.all()[0]
        context['menu'] = self.object.theme.menu.all()
        return context

    def get_template_names(self):
        return self.object.theme.name + '/blog/show.html'


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
