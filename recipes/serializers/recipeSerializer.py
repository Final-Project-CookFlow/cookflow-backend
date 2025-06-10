from rest_framework import serializers
from recipes.models.recipe import Recipe
from recipes.models.category import Category
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer
from users.serializers.userSerializer import CustomUserSerializer

class RecipeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True, source='user_id')
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True, source='step_set')

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
            'updated_at'
        ]

        read_only_fields = ['id','user', 'updated_at']


class RecipeAdminSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True, source='user_id')
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    steps = StepSerializer(many=True, read_only=True, source='step_set')

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
