from .base import AuthorsBaseTest
from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user_test',
            password=string_password
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Usuário de acesso')
        password_field = self.get_by_placeholder(form, 'Senha de acesso')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        form.submit()
        self.assertIn(
            f'Olá { user.first_name }! Você está logado no Masterchef',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
