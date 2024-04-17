from django.urls import path
from .views import create_message, user_chat_rooms, create_chat_room, check_new_messages,get_chat_history

urlpatterns = [
    path('create_message/', create_message, name='create_message'),
    path('user_chat_rooms/<str:user_name>/', user_chat_rooms, name='user_chat_rooms'),
    path('create_chat_room/', create_chat_room, name='create_chat_room'),
    path('check_new_messages/<str:user_name>/', check_new_messages, name='check_new_messages'),
    path('get_chat_history/<int:room_id>/', get_chat_history, name='get_chat_history'),
]