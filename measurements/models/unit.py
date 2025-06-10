from django.conf import settings
from django.db import models
from measurements.models import UnitType


class Unit (models.Model):
    name = models.CharField(max_length=15, unique=True)
    unit_type = models.ForeignKey(settings.AUTH_UNITTYPE_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table = 'units'
