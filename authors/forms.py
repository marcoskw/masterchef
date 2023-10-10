from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


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
        error_messages={
            'required': 'Este campo é obrigatório',
            'max_lenght': 'Este campo não pode ter mais de 65 caracteres',
        },
    )

    password = forms.CharField(
        label='Senha',
        required=True,
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
            raise ValidationError({
                'password': ValidationError(
                    'As senhas não são iguais',
                    code='invalid'
                ),
                'password_verification': 'As senhas não são iguais',
            })
