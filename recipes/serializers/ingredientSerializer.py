from rest_framework import serializers
from recipes.models.ingredient import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'description',
            'quantity',
            'unit',
            'is_checked',
        ]
        read_only_fields = ['id']

class IngredientAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at'] 
    