from django.urls import path
from . import views

urlpatterns = [
    path('look/', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('posts/', views.api_post_list, name='api_post_list'),
]