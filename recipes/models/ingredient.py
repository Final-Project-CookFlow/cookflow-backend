from django.conf import settings
from django.db import models
from .category import Category
from measurements.models import UnitType 


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(
      Category,
      related_name='ingredients',
      db_table='categories_ingredients' 
    )

    class Meta:
        db_table = 'ingredients'
    
    def __str__(self):
        return self.name