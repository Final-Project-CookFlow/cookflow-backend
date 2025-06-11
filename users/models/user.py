# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from media.models import Image # Import the Image model

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    second_surname = models.CharField(max_length=50, null=False)
    # Increased max_length for biography to match common use-cases and Faker output in seeding
    biography = models.CharField(max_length=255, null=True, blank=True) 
    
    # --- ADD THIS LINE FOR PROFILE PICTURE ---
    profile_picture = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL, # If the Image metadata record is deleted, user remains
        null=True,
        blank=True,
        related_name='user_profile_pictures' # Unique related_name for clarity
    )
    # ----------------------------------------
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # Ensure users are active by default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'surname']

    class Meta:
        db_table = 'users'