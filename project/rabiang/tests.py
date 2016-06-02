from django.test import TestCase

from .models import Theme, Site


class ThemeModelTest(TestCase):
    def test_string_representation(self):
        site = Site(name='www')
        theme = Theme(name='default', site=site)
        self.assertEqual(str(theme), theme.name)

    def test_theme_save_read(self):
        site = Site(name='www')
        site.save()
        theme = Theme(name='default', site=site)
        theme.save()

        themes = site.themes.all()

        self.assertEqual(themes[0].name, 'default')
        self.assertEqual(len(themes), 1)

    def test_theme_delete(self):
        site = Site(name='www')
        site.save()
        theme = Theme(name='default', site=site)
        theme.save()

        Theme.objects.get(id=1).delete()

        themes = Theme.objects.all()

        self.assertEqual(len(themes), 0)

    def test_theme_update(self):
        site = Site(name='www')
        site.save()
        theme = Theme(name='default', site=site)
        theme.save()

        t1 = Theme.objects.get(id=1)

        self.assertEqual(t1.name, 'default')

        t1.name = 'main'
        t1.save()

        self.assertEqual(Theme.objects.get(id=1).name, 'main')
