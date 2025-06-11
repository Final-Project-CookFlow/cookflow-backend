from rest_framework import serializers
from media.models.image import Image

class ImageAdminSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    processing_status_display = serializers.CharField(source='get_processing_status_display', read_only=True)

    class Meta:
        model = Image
        fields = [
            'id',
            'name',
            'url',
            'type',
            'type_display',
            'processing_status',
            'processing_status_display',
            'external_id',
            'created_at',
        ]
        read_only_fields = fields

class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'name',
            'url',
            'type',
            'processing_status',
            'external_id'
        ]

class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'url',
            'type',
            'external_id',
            'processing_status'
        ]
        read_only_fields = fields

ImageSerializer = ImageListSerializer 