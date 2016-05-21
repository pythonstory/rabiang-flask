from django.test import TestCase
from .models import Theme, Layout, Site


class ThemeModelTest(TestCase):
    def test_string_representation(self):
        theme = Theme(name='rabiang theme')
        self.assertEqual(str(theme), theme.name)


    def test_theme_save_read(self):
        theme = Theme(name='rabiang theme')
        theme.save()

        themes = Theme.objects.all()

        self.assertEqual(themes[0].name, 'rabiang theme')
        self.assertEqual(len(themes), 1)

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


