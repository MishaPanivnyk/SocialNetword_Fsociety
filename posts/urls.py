from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post_detail'),
    path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment_detail'),
]
