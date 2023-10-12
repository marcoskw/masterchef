from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Usuário de acesso')
        add_placeholder(self.fields['password'], 'Senha de acesso')

    username = forms.CharField(
        label='Usuário',
        error_messages={'required': 'Escreva seu nome'},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha',
        error_messages={
            'required': 'Senha não pode ser vazio'
        },

    )
