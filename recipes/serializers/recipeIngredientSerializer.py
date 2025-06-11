# recipes/serializers/recipeIngredientSerializer.py

from rest_framework import serializers
from recipes.models import RecipeIngredient, Recipe, Ingredient 
from measurements.models import Unit # Ensure Unit model is imported

class RecipeIngredientSerializer(serializers.ModelSerializer):
    # For frontend display: show the name of the ingredient and unit
    ingredient = serializers.CharField(source='ingredient.name', read_only=True)
    # --- FIX APPLIED HERE: unit.name will now correctly access the Unit object's name ---
    unit = serializers.CharField(source='unit.name', read_only=True) 

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit'] 
        read_only_fields = fields 


class RecipeIngredientAdminSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all()) 
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all()) 
    # --- FIX APPLIED HERE: unit should be a PrimaryKeyRelatedField for admin if it's a ForeignKey ---
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False, allow_null=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
        read_only_fields = ('created_at', 'id') 
