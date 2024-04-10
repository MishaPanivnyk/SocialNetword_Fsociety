from django.contrib import admin
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from message import consumers
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')), 
    path('posts/', include('posts.urls')),
    path('friend/', include('friend.urls')), 
]

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