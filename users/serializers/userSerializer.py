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
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        print("Backend: Entering CustomUserLoginSerializer validate method")
        user_input = data.get("identifier")
        password = data.get("password")

        print(f"Backend: Received identifier: '{user_input}'")
        print(f"Backend: Received password (first 3 chars): '{password[:3]}***'") # Mask password for safety

        user_obj = None

        # Try by email
        user_obj_by_email = CustomUser.objects.filter(email=user_input).first()
        print(f"Backend: User found by email: {user_obj_by_email is not None}")
        if user_obj_by_email:
            if user_obj_by_email.check_password(password):
                user_obj = user_obj_by_email
                print("Backend: Password matched for email user.")
            else:
                print("Backend: Password MISMATCH for email user.")

        # If not found or password didn't match by email, try by username
        if not user_obj:
            user_obj_by_username = CustomUser.objects.filter(username=user_input).first()
            print(f"Backend: User found by username: {user_obj_by_username is not None}")
            if user_obj_by_username:
                if user_obj_by_username.check_password(password):
                    user_obj = user_obj_by_username
                    print("Backend: Password matched for username user.")
                else:
                    print("Backend: Password MISMATCH for username user.")

        if user_obj is None:
            print("Backend: No user found or password mismatch after all attempts.")
            raise serializers.ValidationError("Credenciales inválidas.")

        if not user_obj.is_active:
            print(f"Backend: User '{user_obj.username}' is inactive.")
            raise serializers.ValidationError("Usuario inactivo.")

        data["user"] = user_obj
        print(f"Backend: Successfully authenticated user: {user_obj.username}")
        return data


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

class CustomUserFrontSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username'
        ]
        read_only_fields = fields