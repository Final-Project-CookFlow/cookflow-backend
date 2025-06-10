from django.db import models
from django.conf import settings

def default_user():
    return 1 

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=default_user) 
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        return self.name