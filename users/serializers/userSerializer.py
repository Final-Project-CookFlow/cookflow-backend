from rest_framework import serializers
from ..models.user import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'name',
            'surname',
            'second_surname',
            'biography',
            'created_at'
        ]
        read_only_fields = fields


class CustomUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'name',
            'surname',
            'second_surname',
            'biography',
            'password'
        ]

    def validate_password(self, value):
        """
        Valida la fortaleza de la contraseña usando los validadores configurados en Django settings.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_input = data.get("username")
        password = data.get("password")

        user_obj = CustomUser.objects.filter(email=user_input).first() or CustomUser.objects.filter(
            username=user_input).first()

        if user_obj and user_obj.check_password(password):
            if not user_obj.is_active:
                raise serializers.ValidationError("Usuario inactivo.")
            data["user"] = user_obj
            return data

        raise serializers.ValidationError("Credenciales inválidas.")


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'second_surname', 'biography', 'password']

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomUserAdminUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'name', 'surname',
            'second_surname', 'biography', 'is_staff', 'password'
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Sobrescribe el metodo get_token para añadir 'is_staff' y 'is_superuser'.
        """
        token = super().get_token(user)

        # Added fields
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
