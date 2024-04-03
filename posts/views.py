from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user == post.user:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"error": "You don't have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)

        # Перевірка користувача і збереження поста
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user, post=post)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user == comment.user:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"error": "You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)
