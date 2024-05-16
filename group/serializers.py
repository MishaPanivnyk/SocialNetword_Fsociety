from rest_framework import serializers
from .models import Group,GroupMembership
from posts.models import LikeGroup,PostGroup,CommentGroup
from account.models import CustomUser
from django.db import models
from rest_framework import serializers
from .models import Group, GroupMembership
from posts.models import LikeGroup, PostGroup, CommentGroup
from account.models import CustomUser

class CommentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentGroup
        fields = ['id', 'text', 'created_at', 'author']

class LikeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeGroup
        fields = ['id', 'user']

class PostGroupSerializer(serializers.ModelSerializer):
    comments = CommentGroupSerializer(many=True, read_only=True)
    likes = LikeGroupSerializer(many=True, read_only=True)

    class Meta:
        model = PostGroup
        fields = ['id', 'text', 'image', 'created_at', 'author', 'group', 'likes_group', 'comments']

class GroupSerializer(serializers.ModelSerializer):
    posts = PostGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'type', 'image', 'header_image', 'is_staff', 'created_at', 'location', 'members', 'post_count', 'total_likes', 'posts']

class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'group', 'is_admin']
