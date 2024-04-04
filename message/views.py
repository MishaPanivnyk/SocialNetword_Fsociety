# views.py

from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from requests import Response

#class MessageListView(APIView):
   # def post(self, request):
 #       data = request.data
 #       channel_layer = get_channel_layer()
 #       async_to_sync(channel_layer.group_send)(
 #           'chat', {
 #               'type': 'chat_message',
 #               'message': data
 #           }
 #       )
 #       return Response({'status': 'Message sent'}, status=status.HTTP_200_OK)
