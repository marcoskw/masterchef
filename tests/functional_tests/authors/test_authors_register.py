from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/form/div[1]'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register')

        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('teste@teste.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Nome')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.browser.find_element(
                By.XPATH, '/html/body/main/form/div[1]'
            )
            self.assertIn('Escreva seu nome', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Sobrenome')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.browser.find_element(
                By.XPATH, '/html/body/main/form/div[1]'
            )
            self.assertIn('Escreva seu sobrenome', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Usuário')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.browser.find_element(
                By.XPATH, '/html/body/main/form/div[1]'
            )
            self.assertIn('Este campo é obrigatório', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'E-mail')
            email_field.send_keys('teste')
            email_field.send_keys(Keys.ENTER)

            form = self.browser.find_element(
                By.XPATH, '/html/body/main/form/div[1]'
            )
            self.assertIn('Email tem que ser válido', form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password = self.get_by_placeholder(form, 'Senha')
            password_confirmation = self.get_by_placeholder(
                form, 'Repita a senha')
            password.send_keys('Qwe123!@#')
            password_confirmation.send_keys('QweA123!@#')
            password_confirmation.send_keys(Keys.ENTER)

            form = self.browser.find_element(
                By.XPATH, '/html/body/main/form/div[1]'
            )
            self.assertIn('As senhas devem ser iguais', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register')

        form = self.get_form()
        self.get_by_placeholder(
            form, 'Nome').send_keys('Nome')
        self.get_by_placeholder(
            form, 'Sobrenome').send_keys('Sobrenome')
        self.get_by_placeholder(
            form, 'Usuário').send_keys('nome.sobrenome')
        self.get_by_placeholder(
            form, 'E-mail').send_keys('nome.sobrenome@email.com')
        self.get_by_placeholder(
            form, 'Senha').send_keys('Qwe123!@#')
        self.get_by_placeholder(
            form, 'Repita a senha').send_keys('Qwe123!@#')
        form.submit()
        self.assertIn('Usuário criado com sucesso',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
