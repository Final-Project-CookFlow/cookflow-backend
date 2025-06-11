from rest_framework import serializers
from recipes.models import RecipeIngredient, Recipe, Ingredient 
from measurements.models import Unit

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.CharField(source='ingredient.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True) 

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit'] 
        read_only_fields = fields 


class RecipeIngredientAdminSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all()) 
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all()) 
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False, allow_null=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
        read_only_fields = ('created_at', 'id') 
