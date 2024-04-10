from rest_framework import serializers
from .models import Message
from account.serializers import CustomUserSerializer  

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    receiver = CustomUserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']
