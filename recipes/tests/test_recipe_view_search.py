from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
# from unittest import skip


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)
