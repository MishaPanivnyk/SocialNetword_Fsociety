from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')), 
    path('posts/', include('posts.urls')),
    path('friend/', include('friend.urls')), 
    path('chat/', include('chat.urls')), 
    path('reels/', include('reels.urls')),
    path('stories/', include('stories.urls')),
    path('player/', include('player.urls')),
]
