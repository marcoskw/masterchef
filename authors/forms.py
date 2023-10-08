from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    password_verification = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmação de senha'
            }
        ),
        error_messages={
            'required': 'Este campo precisa ser preenchido e igual a senha'
        }
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

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'username': 'Usuário de acesso',

        }

        help_texts = {
            'email': 'O e-mail precisa ser válido',
            'password': 'A senha deve conter letras maiúsculas e minúsculas, numeros e caracteres especiais',  # noqa: 501

        }

        error_messages = {
            'username': {
                'required': 'Este campo é obrigatório',
                'max_lenght': 'Este campo não pode ter mais de 65 caracteres',
            },
        }

        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Senha de acesso'
            })
        }
