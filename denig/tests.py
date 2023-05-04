from django.apps import apps
from django.core import management
from django.test import RequestFactory, SimpleTestCase, TestCase

from denig.models import Collection, Language


class FixtureLoadingTestCase(TestCase):
    def test_loading_languages(self):
        apps.clear_cache()
        management.call_command(
            "loaddata", "denig/fixtures/languages.yaml", verbosity=0
        )
        self.assertSequenceEqual(
            Language.objects.all().values_list("language", flat=True),
            ["English", "German (modern)", "German (old)"],
        )

    def test_loading_libraries(self):
        apps.clear_cache()
        management.call_command(
            "loaddata", "denig/fixtures/collection.yaml", verbosity=0
        )
        self.assertSequenceEqual(
            Collection.objects.all().values_list("library", flat=True),
            ["Winterthur Museum, Garden & Library"],
        )
        self.assertSequenceEqual(
            Collection.objects.all().values_list("location", flat=True),
            ["Winterthur, DE"],
        )
