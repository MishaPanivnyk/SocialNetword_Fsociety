from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Friend
from account.models import CustomUser
from .serializers import FriendSerializer, CustomUserSerializer
from rest_framework import generics
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class FriendSearchView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, name):
        if not name:
            return Response({'error': 'Query parameter "name" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(name, str):
            return Response({'error': 'Query parameter "name" must be a string'}, status=status.HTTP_400_BAD_REQUEST)

        friends = CustomUser.objects.filter(name__icontains=name)
        serializer = CustomUserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    def get(self, request, name):
        user = get_object_or_404(CustomUser, name=name)
        
        user_serializer = CustomUserSerializer(user)
        
        friends = Friend.objects.filter(user=user)
        friends_serializer = FriendSerializer(friends, many=True)
        
        return Response({
            'user_info': user_serializer.data,
            'friends': friends_serializer.data
        }, status=status.HTTP_200_OK)


class AddFriendView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        friend_name = request.data.get('friend_name')
        user_name = request.data.get('user_name')
        
        if not friend_name or not user_name:
            return Response({'error': 'Both "friend_name" and "user_name" are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(friend_name, str) or not isinstance(user_name, str):
            return Response({'error': '"friend_name" and "user_name" must be strings'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(CustomUser, name=user_name)
        friend = get_object_or_404(CustomUser, name=friend_name)
        
        if friend in user.friends.all():
            return Response({'error': 'User is already in your friends list'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship = Friend(user=user, friend=friend, isFollow=True) 
        friendship.save()
        
        user.friends_count += 1
        user.save()

        friend.subscribers_count += 1
        friend.save()
        
        return Response({'message': 'Friend added successfully'}, status=status.HTTP_200_OK)

class RemoveFriendView(APIView):
    #permission_classes = [IsAuthenticated]

    def delete(self, request):
        friend_name = request.data.get('friend_name')
        user_name = request.data.get('user_name')
        
        if not friend_name or not user_name:
            return Response({'error': 'Both "friend_name" and "user_name" are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(friend_name, str) or not isinstance(user_name, str):
            return Response({'error': '"friend_name" and "user_name" must be strings'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(CustomUser, name=user_name)
        friend = get_object_or_404(CustomUser, name=friend_name)
        
        if friend not in user.friends.all():
            return Response({'error': 'User is not in your friends list'}, status=status.HTTP_400_BAD_REQUEST)
        
        Friend.objects.filter(user=user, friend=friend).delete()
        
        user.friends_count -= 1
        user.save()

        friend.subscribers_count -= 1
        friend.save()
        
        return Response({'message': 'Friend removed successfully'}, status=status.HTTP_200_OK)


class AllFriendsView(APIView):
    def get(self, request, user_name):
        user = get_object_or_404(CustomUser, name=user_name)
        friends = user.friends.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowersView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_name):
        user = get_object_or_404(CustomUser, name=user_name)
        followers = Friend.objects.filter(user=user).values_list('friend', flat=True)
        followers_list = CustomUser.objects.filter(id__in=followers)
        serializer = CustomUserSerializer(followers_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class FollowingView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_name):
        user = get_object_or_404(CustomUser, name=user_name)
        following = Friend.objects.filter(user=user).values_list('friend', flat=True)
        following_list = CustomUser.objects.filter(id__in=following)
        serializer = CustomUserSerializer(following_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

