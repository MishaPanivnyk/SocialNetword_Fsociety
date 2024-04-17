from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver']
    search_fields = ['id', 'sender__name', 'receiver__name']
    list_filter = ['sender', 'receiver']
    ordering = ['-id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'sender', 'text', 'timestamp', 'read']  # Виправлено list_display
    search_fields = ['id', 'room__id', 'sender__name', 'text']  # Виправлено search_fields
    list_filter = ['room', 'timestamp', 'read']  # Виправлено list_filter
    ordering = ['-timestamp']
