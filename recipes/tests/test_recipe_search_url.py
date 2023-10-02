from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_search_urls_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
