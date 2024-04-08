from rest_framework import serializers
from account.models import CustomUser
from .models import Friend

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'avatar', 'bio', 'birth_date', 'located',  'friends_count', 'subscribers_count']

class FriendSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    friend = CustomUserSerializer()
    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend', 'isFollow']
