from django.urls import path
from . import views

urlpatterns = [
    path('create_chat/', views.create_chat, name='create_chat'),
    path('get_chat_history/<int:receiver_id>/', views.get_chat_history, name='get_chat_history'),  
    path('get_chat_messages/<int:receiver_id>/', views.get_chat_messages, name='get_chat_messages'),  
]