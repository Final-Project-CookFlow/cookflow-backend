# users/admin.py
from django.contrib import admin
from .models import CustomUser
from .models import Favorite

admin.site.register(CustomUser)
admin.site.register(Favorite)