from django.conf import settings
from django.db import models
from measurements.models import Unit

class ShoppingListItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_shopping_items',
        db_column='user_id'
    )
    ingredient = models.ForeignKey(
        settings.AUTH_INGREDIENT_MODEL,
        on_delete=models.CASCADE,
        related_name='ingredient_shopping_items',
        db_column='ingredient_id'
    )
    quantity_needed = models.IntegerField()
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='unit_shopping_items'
    )
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:    
        db_table = 'shopping_list_items'