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
    
    #Не забудьте також змінити ваш клієнтський код, щоб він міг коректно обробляти ці відповіді, тобто якщо отримано повідомлення, вони відображаються, а якщо таймаут, відбувається повторна відправка запиту.
    #якшо нема нових повідолмень - {"timeout": true}
    #якшо є повідомлення - {"messages": [{"id": 52, "room": 9, "sender": {"email": "Vova1@gmail.com", "name": "Vova1", "avatar": "image/upload/avatar/avatar_S8Ec7Qo.jpg", "bio": "", "birth_date": null, "located": "", "is_active": true, "is_staff": false, "is_email_verified": true, "account_token": "c563wq-24a8e9a2dfd13fa2d0ea5c8c2db28f59", "friends_count": 0, "subscribers_count": 0}, "text": "\u043f\u0440\u0438\u0432\u0456\u0442", "timestamp": "2024-04-18T14:54:00.277325Z", "read": false}]}
    #
    #const checkNewMessages = async () => {
     #       try {
      #          const response = await axios.get('/check_new_messages/username/');
       #         const { data } = response;
        #        if (response.status === 200) {
         #           setMessages(prevMessages => [...prevMessages, ...data.messages]);
          #      }
           # } catch (error) {
            #    if (error.response && error.response.status === 204) {
             #       // Таймаут, повторна відправка запиту через певний час
              #      setTimeout(checkNewMessages, 5000); // Повторна відправка через 5 секунд
               # }

          #             // Початок довгого опитування при монтуванні компонента
        #checkNewMessages();

        #// Очищення таймеру під час розмонтування компонента
        #return () => clearTimeout(checkNewMessages);
    #


def get_chat_history(request, room_id):
    if request.method == 'GET':
        room = get_object_or_404(ChatRoom, id=room_id)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        serialized_messages = MessageSerializer(messages, many=True)
        return JsonResponse(serialized_messages.data, safe=False)
    else:
        return JsonResponse(status=405)
    



    #def check_new_messages(request, user_name):
    #if request.method == 'GET':
   #     user = get_object_or_404(CustomUser, name=user_name)
    #    
        # Отримання всіх непрочитаних повідомлень для користувача
     #   unread_messages = Message.objects.filter(Q(room__sender=user) | Q(room__receiver=user), read=False)
        
        # Серіалізація непрочитаних повідомлень
      #  serialized_messages = MessageSerializer(unread_messages, many=True)
        
       # ids = [message.id for message in unread_messages]

        # Зміна статусу повідомлень на "прочитано" тільки після їх виведення
        #unread_messages1 = Message.objects.filter(id__in=ids, read=False)
        #unread_messages1.update(read=True)
        #print (serialized_messages.data)
       # return JsonResponse(serialized_messages.data, safe=False)
    #else:
     #   return JsonResponse(status=405)