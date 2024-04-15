# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from account.models import CustomUser
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f"chat_user_{self.user.id}"

        # Підключення до кімнати
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Відключення від кімнати
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_name = data['receiver']

        receiver = CustomUser.objects.get(name=receiver_name)

        # Отримання або створення чату
        chat = self.get_or_create_chat(receiver)

        # Збереження повідомлення в базі даних та відправлення всім учасникам чату
        await self.send_and_broadcast_message(chat, message, receiver_name)

        def get_or_create_chat(self, receiver):
            chat = Chat.objects.filter(sender=self.user, receiver=receiver).first()
            if not chat:
                chat = Chat.objects.create(sender=self.user, receiver=receiver)
                return chat

    async def send_and_broadcast_message(self, chat, message, receiver_name):
        # Збереження повідомлення в базі даних
        Message.objects.create(chat=chat, sender=self.user, content=message)

        # Відправлення повідомлення всім учасникам чату
        await self.channel_layer.group_send(
            f"chat_user_{self.user.id}",
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.name,
                'receiver': receiver_name
            }
        )

    async def chat_message(self, event):
        # Відправка повідомлення назад користувачу через WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver']
        }))
