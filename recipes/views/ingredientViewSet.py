from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from recipes.models.ingredient import Ingredient
from recipes.serializers.ingredientSerializer import IngredientSerializer

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Ingredient.objects.filter(is_approved=True)
        recipe_pk = self.kwargs.get('recipe_pk')
        if recipe_pk:
            queryset = queryset.filter(recipe_id=recipe_pk)  # Use your actual FK field name
        return queryset

class IngredientAdminViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminUser]