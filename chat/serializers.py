from rest_framework import serializers
from .models import ChatRoom, Message
from account.serializers import CustomUserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'text', 'timestamp', 'read']

class ChatRoomSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    receiver = CustomUserSerializer()

    class Meta:
        model = ChatRoom
        fields = ['id', 'sender', 'receiver']