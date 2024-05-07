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
<<<<<<< HEAD
    path('player/', include('player.urls')),
    path('group/', include('group.urls')),
=======
>>>>>>> 7ae242180de01a079a62fc14b85665b35f115120
]
