from django.db import models
from django.conf import settings

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField()
    commensals = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(
        "recipes.Category",
        related_name='recipes',
        db_table='categories_recipes'
    )

    class Meta:
        db_table = 'recipes'