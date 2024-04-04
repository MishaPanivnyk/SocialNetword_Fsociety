from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'confirmPassword', 'avatar', 'bio', 'birth_date', 'located', 'is_active', 'is_staff', 'is_email_verified', 'account_token','friends_count','subscribers_count']
        extra_kwargs = {'avatar': {'required': False}}

    def validate(self, attrs):
        if 'password' in attrs and 'confirmPassword' in attrs and attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({'password': 'Паролі повинні співпадати'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        validated_data.pop('confirmPassword', None)
        return super().update(instance, validated_data)
