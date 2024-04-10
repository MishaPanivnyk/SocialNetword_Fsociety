from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import consumers

# Список шляхів WebSocket для споживачів повідомлень
websocket_urlpatterns = [
    path('ws/chat/', consumers.MessageConsumer.as_asgi()),
]


# Основний роутер для WebSocket
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})