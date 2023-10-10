from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha deve conter maiúsculas e minúsculas, números e caracteres especiais'  # noqa 501
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(
        error_messages={'required': 'Escreva o seu nome'},
        label='Nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva o seu sobrenome'},
        label='Sobrenome'
    )
    email = forms.EmailField(
        error_messages={'required': 'Digite um email válido'},
        label='Email',
        help_text='O e-mail precisa ser válido',
    )

    username = forms.CharField(
        label='Usuário de acesso',
        help_text=(
            'Usuário tem que letras, números ou @.+-_'
            'Tem que ter entre 3 e 65 caracteres'
        ),
        error_messages={
            'required': 'Este campo é obrigatório',
            'min_length': 'O usuário precisa ter mais que 2 caracteres',
            'max_length': 'Este campo não pode ter mais de 65 caracteres',
        },
        min_length=2, max_length=65,
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        help_text=('Use uma senha forte'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha de acesso',
            }
        )
    )

    password_verification = forms.CharField(
        label='Confirmação de Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmação de senha',
            }
        ),
        validators=[
            strong_password
        ],
        error_messages={
            'required': 'Este campo precisa ser preenchido e igual a senha'
        },

    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_verification = cleaned_data.get('password_verification')

        if password != password_verification:
            password_confirmation_error = ValidationError(
                'A senha deve conter maiúsculas e minúsculas, números e caracteres especiais, ou senhas não correspondem',  # noqa 501
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password_verification': [password_confirmation_error],
            })
