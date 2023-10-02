from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.recipes.random_factory import make_recipe
from .models import Recipe
from django.http import Http404


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        # 'recipes': [make_recipe() for _ in range(15)],         # example with randon content
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}'
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe,
                               id=id,
                               is_published=True,
                               )

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
    })
