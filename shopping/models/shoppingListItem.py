from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from recipes.models.ingredient import Ingredient

class ShoppingListItem(models.Model):

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(settings.AUTH_INGREDIENT_MODEL, on_delete=models.CASCADE)
    quantity_needed = models.IntegerField()
    unit = models.ForeignKey(settings.AUTH_INGREDIENT_MODEL, on_delete=models.CASCADE)
    is_purchased = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:    
        db_table = 'shopping_list_items'