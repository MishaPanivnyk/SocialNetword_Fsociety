# F_backend/routing.py

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from message.consumers import MessageConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/chat/$", MessageConsumer.as_asgi()),
        ])
    ),
})
