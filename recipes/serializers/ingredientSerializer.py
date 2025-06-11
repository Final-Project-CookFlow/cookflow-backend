# recipes/serializers/ingredientSerializer.py

from rest_framework import serializers
from recipes.models import Ingredient # Import the Ingredient model

class IngredientSerializer(serializers.ModelSerializer):
    # Assuming Ingredient model has these fields directly or via related fields
    # If 'unit' and 'quantity' are part of RecipeIngredient, they don't belong here.
    # This serializer is for the Ingredient model itself, not its use in a recipe.
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'description', # If your Ingredient model has a description
            # 'quantity', # These fields typically belong to RecipeIngredient, not Ingredient itself
            # 'unit',     # Same as above
            # 'is_checked', # This is a frontend state, not a model field
        ]
        read_only_fields = ['id']

class IngredientAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
