from authors.forms import RegisterForm
from django.test import TestCase
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('password', 'Com maiúsculas e minúsculas, números e caracteres especiais'),  # noqa 501
        ('password_verification', 'Confirmação de senha'),
    ])
    def test_password_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
