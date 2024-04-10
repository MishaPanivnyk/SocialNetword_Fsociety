
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from account.models import CustomUser  
from django.db.models import Q

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f"chat_{self.user.id}"  

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create_chat':
            await self.create_or_get_chat(data)
        elif action == 'get_chat_history':
            await self.get_chat_history(data)
        else:
            await self.send(text_data=json.dumps({
                'error': 'Invalid action'
            }))

    async def create_or_get_chat(self, data):
        receiver_id = data['receiver']
        content = data['content']

        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Receiver not found'
            }))
            return

        chat_exists = Message.objects.filter(
            (Q(sender=self.user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=self.user))
        ).exists()

        if not chat_exists:
            message = Message.objects.create(sender=self.user, receiver=receiver, content=content)

            await self.channel_layer.group_send(
                f"chat_{receiver_id}",
                {
                    'type': 'chat_message',
                    'sender': self.user.id,
                    'receiver': receiver_id,
                    'content': content
                }
            )
        else:
            await self.create_chat(data)

    async def get_chat_history(self, data):
        receiver_id = data['receiver']
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Receiver not found'
            }))
            return

        messages = Message.objects.filter(
            (Q(sender=self.user) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=self.user))
        ).order_by('timestamp')

        history = [{
            'sender': msg.sender.id,
            'receiver': msg.receiver.id,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]

        await self.send(text_data=json.dumps({
            'action': 'chat_history',
            'history': history
        }))
