from django.conf import settings
from django.db import models
from .recipe import Recipe 

class Step(models.Model):
    order = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) # Use Recipe directly
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'steps'