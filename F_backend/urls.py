from django.contrib import admin
from django.urls import path, include
from message import routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')), 
    path('posts/', include('posts.urls')),
    path('friend/', include('friend.urls')), 
    path('', include(routing.websocket_urlpatterns)), 
]
