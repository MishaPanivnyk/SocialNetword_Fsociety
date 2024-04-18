from django.urls import path
from . import views

urlpatterns = [
path('look/', views.look_post_list_all, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('lookPostUser/<str:author_identifier>/', views.look_post_list_user, name='look_post_list_user'),
    path('like/', views.like_post, name='like_post'),
    path('unlike/', views.unlike_post, name='unlike_post'),
    path('comment/', views.comment_post, name='comment_post'),
    path('delete/', views.delete_post, name='delete_post'),
    #path('delete_comment/', views.delete_comment, name='delete_comment'),
]
