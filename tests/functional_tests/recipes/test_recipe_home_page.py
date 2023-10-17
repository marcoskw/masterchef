import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Sem receitas para mostrar :-(', body.text)

    def test_recipe_search_input_can_find_correct_recipe(self):
        title_needed = 'Title of Recipe'

        recipes = self.make_recipe_in_bath()

        recipes[0].title = 'Title of Recipe'
        recipes[0].save()

        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Procurar por uma receita..."]')

        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(title_needed, self.browser.find_element(
            By.CLASS_NAME, 'main-content-list').text)
