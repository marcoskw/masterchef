from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('title'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')
        add_attr(self.fields.get('preparation_ingredients'), 'class', 'span-2')
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('category'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_ingredients',
            'preparation_steps',
            'cover',
            'category',
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Unidades', 'Unidades'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append(
                'O titulo não pode ser igual a descrição')
            self._my_errors['description'].append(
                'A descrição não pode ser igual ao título')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        field_name = 'title'

        field_value = self.cleaned_data.get(field_name)
        if len(field_value) < 5:
            self._my_errors[field_name].append(
                'O titulo precisa ter mais que 5 caracteres')
        return field_value

    def clean_preparation_time(self):
        field_name = 'preparation_time'

        field_value = self.cleaned_data.get(field_name)
        if is_positive_number(field_name):
            self._my_errors[field_name].append(
                'O campo precisa ser um número inteiro positivo!')
        return field_value

    def clean_servings(self):
        field_name = 'servings'

        field_value = self.cleaned_data.get(field_name)
        if is_positive_number(field_name):
            self._my_errors[field_name].append(
                'O campo precisa ser um número inteiro positivo!')
        return field_value
