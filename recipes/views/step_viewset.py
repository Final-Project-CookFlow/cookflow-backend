from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly, IsAdminUser, SAFE_METHODS
from recipes.models.step import Step
from recipes.serializers.stepSerializer import StepSerializer, StepAdminSerializer

class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS and self.request.user and self.request.user.is_staff:
            return StepAdminSerializer
        return StepSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAuthenticated()]
    
    def get_queryset(self):
        recipe_id = self.request.query_params.get('recipe_id')
        if recipe_id:
            return Step.objects.filter(recipe__id=recipe_id)
        return super().get_queryset()

class StepAdminViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepAdminSerializer
    permission_classes = [IsAdminUser]
