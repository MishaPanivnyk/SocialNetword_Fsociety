from django.urls import path
from . import views

urlpatterns = [
    path('look/', views.look_post_list_all, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('lookPostUser/<str:author_identifier>/', views.look_post_list_user, name='look_post_list_user')
]