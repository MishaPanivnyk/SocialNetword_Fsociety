from django.urls import path
from .views import FriendSearchView, UserProfileView, AddFriendView, RemoveFriendView, AllFriendsView, FollowersView, FollowingView

urlpatterns = [
    path('search/<str:name>/', FriendSearchView.as_view(), name='friend-search'),
    path('profile/<str:name>/', UserProfileView.as_view(), name='user-profile'),
    path('add/', AddFriendView.as_view(), name='add-friend'),
    path('remove/', RemoveFriendView.as_view(), name='remove-friend'),
    path('search/all/<str:user_name>/', AllFriendsView.as_view(), name='all-friends'),
    path('followers/<str:user_name>/', FollowersView.as_view(), name='followers-list'),
    path('following/<str:user_name>/', FollowingView.as_view(), name='following-list'),
]
