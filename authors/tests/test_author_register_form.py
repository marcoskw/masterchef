from unittest import TestCase
from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Usuário'),
        ('email', 'E-mail'),
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('password', 'Senha'),
        ('password_verification', 'Repita a senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', (
            'Usuário tem que letras, números ou @.+-_'
            'Tem que ter entre 3 e 65 caracteres'
        )),
        ('email', 'Email tem que ser válido'),
        ('password', (
            'Senha tem que ter letra maiúscula, minúscula, '
            'número e caracter especial. E tamanho mínimo '
            'de 8 caracteres'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Usuário'),
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password_verification', 'Confirmação de Senha'),
    ])
    def test_fields_label(self, field, needed):
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
            'password': '1',
            'password_verification': '1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
        ('first_name', 'Escreva seu nome'),
        ('last_name', 'Escreva seu sobrenome'),
        ('password', 'Senha não pode ser vazio'),
        ('password_verification', 'Por favor, repita sua senha'),
        ('email', 'E-mail obrigarório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_2(self):
        self.form_data['username'] = 'j'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'O usuário precisa ter mais que 2 caracteres'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_65(self):
        self.form_data['username'] = 'A' * 67
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Este campo não pode ter mais de 65 caracteres'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'A senha deve conter maiúsculas e minúsculas, '
            'números e caracteres especiais'
        )

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password_verification'] = '@A123abc1235'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas devem ser iguais'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password_verification'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
