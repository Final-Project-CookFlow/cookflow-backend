import random
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from recipes.models.recipe import Recipe
from recipes.serializers.recipeSerializer import RecipeSerializer, RecipeAdminSerializer, RandomRecipePublicSerializer
from media.services.image_service import update_image_for_instance
from users.models import Favorite


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Recipe.

    Usuarios autenticados pueden realizar todas las operaciones CRUD.
    Usuarios NO autenticados solo pueden hacer GET (listar y ver recetas).

    Attributes:
        queryset (QuerySet): Obtiene todos los objetos Recipe.
        permission_classes (list): Controla el acceso según autenticación.
        get_serializer_class (func): Selecciona el serializer según el tipo de usuario.

    Author:
        {Lorena Martínez}
    """
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return RecipeAdminSerializer
        return RecipeSerializer

    def perform_create(self, serializer): 
        recipe = serializer.save(user_id=self.request.user)

        image_file = self.request.FILES.get("recipe_image")
        if image_file:
            update_image_for_instance(
                image_file=image_file,
                user_id=self.request.user.id,
                external_id=recipe.id,
                image_type="RECIPE"
            )

    @action(detail=False, methods=['get'])
    def random(self, request):
        user = request.user
        count = int(request.query_params.get('count', 5))

        favorited_recipe_ids = Favorite.objects.filter(user_id=user).values_list('recipe_id', flat=True)
        available_recipes_qs = Recipe.objects.exclude(id__in=favorited_recipe_ids).prefetch_related('categories')

        available_recipe_ids = list(available_recipes_qs.values_list('id', flat=True))

        if not available_recipe_ids:
            return Response([])

        num_to_select = min(count, len(available_recipe_ids))
        random_ids = random.sample(available_recipe_ids, num_to_select)

        random_recipes = available_recipes_qs.filter(id__in=random_ids)
        serializer = RandomRecipePublicSerializer(random_recipes, many=True)

        return Response(serializer.data)
