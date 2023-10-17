from recipes import views
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch
# from unittest import skip


class RecipeHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_founds_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>Sem receitas para mostrar :-(</h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipefor this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Test Title', content)
        self.assertIn('10 test', content)
        self.assertIn('5 test', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dint_load_recipes_not_published(self):
        """Test recipe is_published False don't show"""
        # Need a recipefor this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if one recipe exists
        self.assertIn(
            '<h1>Sem receitas para mostrar :-(</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_bath(qtd=8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_bath(qtd=8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )

            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
