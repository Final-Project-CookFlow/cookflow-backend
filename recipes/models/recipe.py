from django.db import models
from django.conf import settings
from media.models.image import Image

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

    main_photo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_recipe_photo'
    )

    class Meta:
        db_table = 'recipes'

    def __str__(self):
        return self.name