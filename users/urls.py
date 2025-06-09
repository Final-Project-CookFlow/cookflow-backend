from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views.userView import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    AdminUserViewSet,
    UserFavoriteListCreateView,
    UserFavoriteDestroyView,
    AdminFavoriteViewSet
)

urlpatterns = [
    # Auth and user routes
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/me/', UserProfileView.as_view(), name='user-profile-me'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile-detail'),

    # User administration routes
    path('admin/users/', AdminUserViewSet.as_view(), name='admin-user-list-create'),
    path('admin/users/<int:pk>/', AdminUserViewSet.as_view(), name='admin-user-detail-update-destroy'),

    # Favorite routes for auth user
    path('favorites/', UserFavoriteListCreateView.as_view(), name='user-favorite-list-create'),
    path('favorites/<int:pk>/', UserFavoriteDestroyView.as_view(), name='user-favorite-destroy'),

    # Routes for favorites administration
    path('admin/favorites', AdminFavoriteViewSet.as_view(), name='admin-favorite-list-create'),
    path('admin/favorites/<int:pk>/', AdminFavoriteViewSet.as_view(), name='admin-favorite-detail-update-destroy'),

    # Routes for get and refresh JWT tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obatin_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
