from django.contrib.auth.models import User
from django.db import models
from account.models import CustomUser

class ChatRoom(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender_rooms', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='receiver_rooms', on_delete=models.CASCADE)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)