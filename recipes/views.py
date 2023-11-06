import os
from django.http import Http404
# from utils.recipes.random_factory import make_recipe
from django.db.models import Q
from .models import Recipe
from utils.pagination import make_pagination
from django.views.generic import ListView, DetailView
# from django.contrib import messages


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            is_published=True
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_object, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )
        context.update({
            'recipes': page_object,
            'pagination_range': pagination_range
        })
        return context


class RecipeListViewHome(RecipeListView):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListView):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title':
                f'{context.get("recipes")[0].category.name} - Categoria | '
        })

        return context


class RecipeListViewSearch(RecipeListView):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),

            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        page_object, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )
        context.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'recipes': page_object,
            'pagination_range': pagination_range,
            'additional_url_query': f'&q={search_term}'
        })
        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            is_published=True
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'is_detail_page': True,
        })

        return context
