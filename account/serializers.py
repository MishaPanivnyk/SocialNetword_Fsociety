from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'confirmPassword', 'avatar']
        extra_kwargs = {'avatar': {'required': False}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({'password': 'Паролі повинні співпадати'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        user = CustomUser.objects.create_user(**validated_data)
        return user
