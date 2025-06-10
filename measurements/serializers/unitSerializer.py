from rest_framework import serializers
from measurements.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name', 'unit_type')
        read_only_fields = ('id', 'name', 'unit_type')

class UnitAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('created_at', 'id')
        extra_kwargs = {
            'name': {'required': True, 'max_length': 15},
            'unit_type': {'required': True},
        }