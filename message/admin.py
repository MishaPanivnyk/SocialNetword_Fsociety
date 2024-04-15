from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'timestamp']  
    list_filter = ['timestamp']  

admin.site.register(Message, MessageAdmin)