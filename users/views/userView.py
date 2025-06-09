from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from ..models.user import CustomUser
from ..serializers.userSerializer import (
    CustomUserSerializer,
    CustomUserAdminSerializer,
    CustomUserCreateSerializer,
    CustomUserLoginSerializer,
    CustomUserUpdateSerializer,
    CustomUserAdminUpdateSerializer
)
from ..models.favorite import Favorite
from ..serializers.favoriteSerializer import (
    FavoriteSerializer,
    FavoriteAdminSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # <-- Log errors here
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Access without auth

    def post(self, request, *_args, **_kwargs):
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # If auth fails, raises an exception

        user = serializer.validated_data.get("user")  # The serializer has already validated and got the user

        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()  # It will be used for lookup, but get_object is overridden
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # For the URL /users/me/
        if self.kwargs.get('pk') == 'me':
            return self.request.user

        # For the URL /users/{pk}/, ensure the PK corresponds to the logged-in user
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if obj != self.request.user:
            self.permission_denied(
                self.request,
                message="No tienes permiso para acceder a este perfil."
            )
        return obj

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserSerializer  # To view the profile (read-only).
        return CustomUserUpdateSerializer  # To update the profile.


class AdminUserViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]  # Only is_staff users can access

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserAdminSerializer  # To list and view user details by admin
        elif self.request.method == 'POST':
            return CustomUserCreateSerializer  # To create a new user by admin (using the creation serializer)
        return CustomUserAdminUpdateSerializer  # To update users by admin


# Favorite views

class UserFavoriteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class UserFavoriteDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user_id=self.request.user)


class AdminFavoriteViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = FavoriteAdminSerializer
