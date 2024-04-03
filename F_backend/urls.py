
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')), 
    path('posts/', include('posts.urls')),
    path('friend/', include('friend.urls')),
    path('message/', include('message.urls')),
    path(r'', include('app_blog.urls')),
]
