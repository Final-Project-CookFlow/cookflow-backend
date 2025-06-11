# recipes/serializers/recipeSerializer.py
from rest_framework import serializers
from recipes.models import Recipe, Category, Step, RecipeIngredient
from .stepSerializer import StepSerializer
from .recipeIngredientSerializer import RecipeIngredientSerializer
from users.serializers.userSerializer import CustomUserSerializer
from media.serializers.imageSerializer import ImageSerializer

class RecipeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True) 
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    image_url = serializers.CharField(source='main_photo.url', read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'user',
            'duration_minutes',
            'commensals',
            'categories',
            'steps',
            'recipe_ingredients',
            'updated_at',
            'image_url',
        ]
        read_only_fields = ['id', 'user', 'updated_at']

class RecipeAdminSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipeingredient_set') # Using the RecipeIngredientSerializer for nesting

    image_url = serializers.CharField(source='main_photo.url', read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']