# recipes/step.py
from django.db import models
from media.models import Image
from .recipe import Recipe

class Step(models.Model):
    order = models.IntegerField()
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='step_images'
    )
    
    # -------------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'steps'
        unique_together = ('recipe', 'order') # Good practice: ensure unique step order per recipe

    def __str__(self):
        return f"Step {self.order} for {self.recipe.name}"