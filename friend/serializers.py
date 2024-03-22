from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friend

class FriendSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    friend_username = serializers.ReadOnlyField(source='friend.username')

    class Meta:
        model = Friend
        fields = ['id', 'user', 'user_username', 'friend', 'friend_username', 'date_added']
