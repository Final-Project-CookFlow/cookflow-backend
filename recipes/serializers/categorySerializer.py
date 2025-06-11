# recipes/serializers/categorySerializer.py

from rest_framework import serializers
from recipes.models import Category, Ingredient, Recipe # Import necessary models
from .recipeSerializer import RecipeSerializer # Import RecipeSerializer
from .ingredientSerializer import IngredientSerializer # Import IngredientSerializer

class CategorySerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True) # Assumes Category has a reverse relation to Ingredient
    # recipes = RecipeSerializer(many=True, read_only=True) # Uncomment if you want nested recipes here, but can be verbose

    class Meta:
        model = Category
        fields = ['id', 'name', 'user_id', 'parent_category_id', 'ingredients'] # Removed 'recipes' for conciseness
        read_only_fields = fields

class CategoryAdminSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True) # Admin might want full recipe details
    ingredients = IngredientSerializer(many=True, read_only=True) # Admin might want full ingredient details

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
