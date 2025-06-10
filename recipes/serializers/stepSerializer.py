from rest_framework import serializers
from recipes.models import Step, Recipe

class StepSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    class Meta:
        model = Step
        fields = ('order', 'description', 'id', 'recipe_id','created_at', 'updated_at')  
        read_only_fields = ('id','created_at', 'updated_at')

class StepAdminSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True) 
    class Meta:
        model = Step
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'id')