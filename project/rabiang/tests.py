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

        themes = site.themes

        self.assertEqual(themes[0].name, 'default')
        self.assertEqual(len(themes), 1)

    """
    def test_theme_delete(self):
        theme = Theme(name='rabiang theme')
        theme.save()

        Theme.objects.get(id=1).delete()

        themes = Theme.objects.all()

        self.assertEqual(len(themes), 0)

    def test_theme_update(self):
        theme = Theme(name='rabiang theme')
        theme.save()

        t1 = Theme.objects.get(id=1)

        self.assertEqual(t1.name, 'rabiang theme')

        t1.name = 'another theme'
        t1.save()

        self.assertEqual(Theme.objects.get(id=1).name, 'another theme')
    """
