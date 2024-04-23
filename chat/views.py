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

        # Перевіряємо, чи існує чат-кімната з цими двома користувачами
        existing_room = ChatRoom.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        ).first()

        if existing_room:
            # Якщо кімната вже існує, повертаємо інформацію про неї
            return JsonResponse({'room_id': existing_room.id, 'sender': sender_name, 'receiver': receiver_name}, status=200)
        else:
            # Якщо кімната ще не існує, створюємо нову
            room = ChatRoom.objects.create(sender=sender, receiver=receiver)
            Message.objects.create(room=room, sender=sender, text="Room created", read=False)
            return JsonResponse({'room_id': room.id, 'sender': sender_name, 'receiver': receiver_name}, status=201)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def create_message(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        text = request.POST.get('text')
        sender_name = request.POST.get('sender_name')

        room = get_object_or_404(ChatRoom, id=room_id)
        sender = get_object_or_404(CustomUser, name=sender_name)

        # Перевіряємо, чи sender або receiver є поточним користувачем,
        # і встановлюємо receiver в залежності від цього
        if room.sender == sender:
            receiver = room.receiver
        elif room.receiver == sender:
            receiver = room.sender
        else:
            # Якщо sender не є ні sender, ні receiver кімнати, повертаємо помилку
            return JsonResponse({'error': 'Invalid sender for this room'}, status=400)

        # Створюємо повідомлення, встановлюємо receiver відповідно
        message = Message.objects.create(room=room, sender=sender, receiver=receiver, text=text, read=False)

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
        
        TIMEOUT = 5
        
        # Очікування нових повідомлень протягом тривалого періоду часу
        new_messages = Message.objects.filter(receiver=user, read=False).exists()
        
        if new_messages:
            # Отримання нових повідомлень
            unread_messages = Message.objects.filter(receiver=user, read=False)
            serialized_messages = MessageSerializer(unread_messages, many=True)
            ids = [message.id for message in unread_messages]
            # Оновлення статусу повідомлень
            unread_messages1 = Message.objects.filter(id__in=ids, read=False)
            unread_messages1.update(read=True)
            return JsonResponse({'messages': serialized_messages.data}, status=200)
        else:
            # Таймаут, якщо немає нових повідомлень
            return JsonResponse({}, status=204)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    


def get_chat_history(request, room_id):
    if request.method == 'GET':
        room = get_object_or_404(ChatRoom, id=room_id)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        serialized_messages = MessageSerializer(messages, many=True)
        return JsonResponse(serialized_messages.data, safe=False)
    else:
        return JsonResponse(status=405)
    