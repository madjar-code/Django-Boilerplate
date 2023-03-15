from django.contrib import auth
from rest_framework import serializers
from rest_framework.serializers import\
    Serializer, ModelSerializer
from rest_framework.exceptions import\
    AuthenticationFailed
from users.models import User


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=2, write_only=True)
    
    class Meta:
        model = User
        fields = (
            'email',
            'password',            
        )

    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(max_length=68, min_length=2, write_only=True)
    access = serializers.CharField(max_length=68, min_length=6, read_only=True)
    refresh = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'access',
            'refresh',
        )

    def validate(self, attrs):
        """During validation, authentication occurs on the backend"""
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']}


class ChangePasswordSerializer(Serializer):
    """
    Serializer for password change endpoint
    """
    model = User
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
