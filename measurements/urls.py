from rest_framework.routers import DefaultRouter
from measurements.views.measurementView import UnitViewSet, UnitTypeViewSet

router = DefaultRouter()
router.register(r'units', UnitViewSet)
router.register(r'unit-types', UnitTypeViewSet)

urlpatterns = router.urls