from django.db import models
from .recipe import Recipe 
from .ingredient import Ingredient 
from measurements.models import Unit # Import the Unit model

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipes")
    quantity = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name="recipe_units")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recipe_ingredients'