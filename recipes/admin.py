from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        'category',
        'created_at',
        'is_published',

    ]

    list_display_links = [
        'title',
        'created_at',
    ]

    search_fields = [
        'id',
        'title',
        'category',
        'description',
        'slug',
    ]

    list_filter = [
        'category',
        'author',
        'is_published',
    ]

    list_per_page = 30

    list_editable = [
        'is_published'
    ]

    ordering = [
        '-id'
    ]

    prepopulated_fields = {
        "slug": ('title',)
    }

    autocomplete_fields = 'tags',


admin.site.register(Category, CategoryAdmin)
