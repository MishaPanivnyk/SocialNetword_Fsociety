from django.urls import path
from .views import ReelView

reel_view = ReelView()

urlpatterns = [
    path('create/', reel_view.create_reel, name='create_reel'),
    path('like/', reel_view.like_reel, name='like_reel'),
    path('comment/', reel_view.comment_reel, name='comment_reel'),
    path('delete_comment/', reel_view.delete_comment, name='delete_comment'),
    path('unlike/', reel_view.unlike_reel, name='unlike_reel'),
    path('reelsUser/<str:author_identifier>/', reel_view.look_reel_list_user, name='look_reel_list_user'),
    path('reelsAll/<str:author_identifier>/', reel_view.look_reel_list_all, name='look_reel_list_all'),
]