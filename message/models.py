from django.db import models
from django.conf import settings
from account.models import CustomUser 

class Chat(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_chats', on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} in {self.chat}: {self.content}"
     