# recipes/admin.py
from django.contrib import admin
from .models import Recipe, Step, Category, Ingredient, RecipeIngredient # Add other models as needed

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient) 