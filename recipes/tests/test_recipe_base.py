from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeMixin:
    def make_category(
            self,
            name='Category'
    ):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='user@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Test Title',
        description='Recipe Test Description',
        slug='recipe-test-slug',
        preparation_time='10',
        preparation_time_unit='test',
        servings='5',
        servings_unit='test',
        preparation_ingredients='1 Test, 2 Test',
        preparation_steps='1 Test, 2 Test, 3 Test',
        is_published=True,
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_ingredients=preparation_ingredients,
            preparation_steps=preparation_steps,
            is_published=is_published,
        )


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
