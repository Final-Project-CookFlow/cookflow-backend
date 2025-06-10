from rest_framework import serializers
from measurements.models import UnitType
from .unitSerializer import UnitSerializer

class UnitTypeSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    class Meta:
        model = UnitType
        fields = ('name', 'units')
        read_only_fields = ('name', 'units')

class UnitTypeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = ('name', 'units')
        read_only_fields = ('name', 'units')
        extra_kwargs = {
            'name': {'required': True, 'max_length': 15},
        }