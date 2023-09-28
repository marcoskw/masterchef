from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
# from unittest import skip


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'CategoryTest'
        # Need a recipefor this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dint_load_recipes_not_published(self):
        """Test recipe is_published False don't show"""
        # Need a recipefor this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': recipe.category.id}
            )
        )

        # Check if one recipe exists
        self.assertEqual(response.status_code, 404)
