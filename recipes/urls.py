from rest_framework_nested import routers
from django.urls import path, include
from recipes.views.recipeView import RecipeViewSet
from recipes.views.ingredientViewSet import IngredientViewSet, IngredientAdminViewSet
from recipes.views.step_viewset import StepViewSet, StepAdminViewSet
from recipes.views.categoryView import CategoryView

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'admin/ingredients', IngredientAdminViewSet, basename='ingredient-admin')
router.register(r'steps', StepViewSet, basename='step')
router.register(r'admin/steps', StepAdminViewSet, basename='step-admin')
router.register(r'categories', CategoryView, basename='category')

recipes_router = routers.NestedDefaultRouter(router, r'recipes', lookup='recipe')
recipes_router.register(r'ingredients', IngredientViewSet, basename='recipe-ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(recipes_router.urls)),
]