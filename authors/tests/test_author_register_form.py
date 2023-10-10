from authors.forms import RegisterForm
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('password', 'Senha de acesso'),  # noqa 501
        ('password_verification', 'Confirmação de senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, placeholder)

    @parameterized.expand([
        ('email', 'O e-mail precisa ser válido'),
        ('password', 'Use uma senha forte'),
        ('username', ('Usuário tem que letras, números ou @.+-_'
                      'Tem que ter entre 3 e 65 caracteres')),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'Email'),
        ('username', 'Usuário de acesso'),
        ('password', 'Senha'),
        ('password_verification', 'Confirmação de Senha'),
    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Qwe123!@#',
            'password_verification': 'Qwe123!@#',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
        ('first_name', 'Escreva o seu nome'),
        ('last_name', 'Escreva o seu sobrenome'),
        ('email', 'Digite um email válido'),
        ('password', 'A senha deve conter maiúsculas e minúsculas, números e caracteres especiais, ou senhas não correspondem'),  # noqa 501
        ('password_verification', 'Este campo precisa ser preenchido e igual a senha'),  # noqa 501
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'A senha deve conter maiúsculas e minúsculas, números e caracteres especiais, ou senhas não correspondem'  # noqa 501

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = ''
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password_verification'] = '@A123abc1235'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'A senha deve conter maiúsculas e minúsculas, números e caracteres especiais, ou senhas não correspondem'  # noqa 501

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password_verification'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'A senha deve conter maiúsculas e minúsculas, números e caracteres especiais, ou senhas não correspondem'  # noqa 501
        self.assertNotIn(msg, response.content.decode('utf-8'))
