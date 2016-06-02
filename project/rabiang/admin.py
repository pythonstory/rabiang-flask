from django.contrib import admin

from .models import Site, Theme, Menu, MenuItem, Module, Document, Comment

admin.site.register(Site)
admin.site.register(Theme)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Module)
admin.site.register(Document)
admin.site.register(Comment)
