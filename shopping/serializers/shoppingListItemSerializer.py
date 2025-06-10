from rest_framework import serializers
from shopping.models.shoppingListItem import ShoppingListItem
from measurements.serializers import UnitSerializer

class ShoppingListItemSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user', 
        read_only=True
    )
    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient', 
        read_only=True
    )
    unit_details = UnitSerializer(
        source='unit', 
        read_only=True
    )

    class Meta:
        model = ShoppingListItem
        fields = [
            'id',
            'user_id',
            'ingredient_id',
            'quantity_needed',
            'unit',
            'unit_details', 
            'is_purchased',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'user_id',
            'ingredient_id',
            'unit_details',
            'created_at'
        ]

class ShoppingListItemAdminSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        read_only=True
    )
    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )

    unit_details = UnitSerializer(
        source='unit',
        read_only=True
    )

    class Meta:
        model = ShoppingListItem
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'user_id',
            'ingredient_id',
            'unit_details'
        ]