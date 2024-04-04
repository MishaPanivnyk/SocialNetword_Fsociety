import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class MessageConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.scope['user']
        receiver = data['receiver']
        content = data['content']

        message = Message.objects.create(sender=sender, receiver=receiver, content=content)

        # Надіслати повідомлення до групи кімнати
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.id,
                'receiver': receiver,
                'content': content
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
