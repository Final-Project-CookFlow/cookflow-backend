from rest_framework import serializers
from recipes.models.category import Category
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.serializers.recipeSerializer import RecipeSerializer
from recipes.serializers.ingredientSerializer import IngredientSerializer


class CategorySerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:

        model = Category
        fields = ['id', 'name', 'user_id', 'parent_category_id', 'recipes', 'ingredients']
        read_only_fields = ['id', 'name', 'user_id', 'parent_category_id', 'recipes', 'ingredients']

class CategoryAdminSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
