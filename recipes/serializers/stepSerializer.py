# recipes/serializers/stepSerializer.py

from rest_framework import serializers
from recipes.models import Step # Import the Step model
from media.serializers.imageSerializer import ImageSerializer # Correct import for ImageSerializer

class StepSerializer(serializers.ModelSerializer):
    # 'image' is a ForeignKey to an Image object, so we nest the ImageSerializer.
    # This will return the entire serialized Image object (e.g., {'id': 1, 'url': 'http://...', 'type': 'STEP'}).
    image = ImageSerializer(read_only=True) 

    class Meta:
        model = Step
        fields = ('order', 'description', 'id', 'recipe_id', 'image', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class StepAdminSerializer(serializers.ModelSerializer):
    # For admin, typically you'd want to select an existing Image object by its ID for a ForeignKey.
    # Or, if you have a custom admin field for file upload that saves to Image model, you'd handle that.
    # This assumes linking to an existing Image instance by its primary key.
    image = serializers.PrimaryKeyRelatedField(
        queryset=ImageSerializer.Meta.model.objects.all(), # Get queryset from ImageSerializer's model
        required=False,
        allow_null=True
    )

    class Meta:
        model = Step
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'id')
