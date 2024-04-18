from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from account.models import CustomUser
from chat.models import ChatRoom, Message
from chat.serializers import MessageSerializer, ChatRoomSerializer
from rest_framework import status
from django.db.models import Q
from django.db.models import F

def create_chat_room(request):
    if request.method == 'POST':
        sender_name = request.POST.get('sender_name')
        receiver_name = request.POST.get('receiver_name')

        sender = get_object_or_404(CustomUser, name=sender_name)
        receiver = get_object_or_404(CustomUser, name=receiver_name)

        room = ChatRoom.objects.create(sender=sender, receiver=receiver)

        # Записуємо дані у базу даних
        Message.objects.create(room=room, sender=sender, text="Room created", read=False)

        return JsonResponse({'room_id': room.id, 'sender': sender_name, 'receiver': receiver_name}, status=201)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def create_message(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        text = request.POST.get('text')

        room = get_object_or_404(ChatRoom, id=room_id)
        sender = room.sender
        receiver = room.receiver

        message = Message.objects.create(room=room, sender=sender, text=text, read=False)

        return JsonResponse({'message_id': message.id}, status=201)
    else:
        return JsonResponse(status=405)

def user_chat_rooms(request, user_name):
    if request.method == 'GET':
        user = get_object_or_404(CustomUser, name=user_name)
        sender_rooms = ChatRoom.objects.filter(sender=user)
        receiver_rooms = ChatRoom.objects.filter(receiver=user)
        rooms = sender_rooms | receiver_rooms
        serialized_rooms = ChatRoomSerializer(rooms, many=True)
        return JsonResponse(serialized_rooms.data, safe=False) 
    else:
        return JsonResponse(status=405)
#unread_messages.update(read=True)

def check_new_messages(request, user_name):
    if request.method == 'GET':
        user = get_object_or_404(CustomUser, name=user_name)
        
        # Отримання всіх непрочитаних повідомлень для користувача
        unread_messages = Message.objects.filter(Q(room__sender=user) | Q(room__receiver=user), read=False)
        
        # Серіалізація непрочитаних повідомлень
        serialized_messages = MessageSerializer(unread_messages, many=True)
        
        ids = [message.id for message in unread_messages]

        # Зміна статусу повідомлень на "прочитано" тільки після їх виведення
        unread_messages1 = Message.objects.filter(id__in=ids, read=False)
        unread_messages1.update(read=True)
        #print (serialized_messages.data)
        return JsonResponse(serialized_messages.data, safe=False)
    else:
        return JsonResponse(status=405)
    
    

def get_chat_history(request, room_id):
    if request.method == 'GET':
        room = get_object_or_404(ChatRoom, id=room_id)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        serialized_messages = MessageSerializer(messages, many=True)
        return JsonResponse(serialized_messages.data, safe=False)
    else:
        return JsonResponse(status=405)