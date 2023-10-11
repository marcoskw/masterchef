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
            'A senha deve conter maiúsculas e '
            'minúsculas, números e caracteres especiais'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Usuário')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['first_name'], 'Nome')
        add_placeholder(self.fields['last_name'], 'Sobrenome')
        add_placeholder(self.fields['password'], 'Senha')
        add_placeholder(self.fields['password_verification'], 'Repita a senha')

    username = forms.CharField(
        label='Usuário',
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
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu nome'},
        label='Nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Sobrenome'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail obrigarório'},
        label='E-mail',
        help_text='Email tem que ser válido',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Senha não pode ser vazio'
        },
        help_text=(
            'Senha tem que ter letra maiúscula, minúscula, '
            'número e caracter especial. E tamanho mínimo '
            'de 8 caracteres'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password_verification = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmação de Senha',
        error_messages={
            'required': 'Por favor, repita sua senha'
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Este email já está cadastrado',
                code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_verification = cleaned_data.get('password_verification')

        if password != password_verification:
            password_confirmation_error = ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password_verification': [
                    password_confirmation_error,
                ],
            })
