from rest_framework import serializers
from account.serializers import CustomUserSerializer
from .models import Friend
from account.models import CustomUser


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'avatar', 'bio', 'birth_date', 'located', 'is_email_verified', 'friends_count']
