from django.urls import path
from .views import FriendSearchView, UserProfileView, AddFriendView, RemoveFriendView , AllFriendsView

urlpatterns = [
    path('search/<str:name>/', FriendSearchView.as_view(), name='friend-search'),
    path('profile/<str:name>/', UserProfileView.as_view(), name='user-profile'),
    path('add/', AddFriendView.as_view(), name='add-friend'),
    path('remove/', RemoveFriendView.as_view(), name='remove-friend'),
    path('all/<str:user_name>/', AllFriendsView.as_view(), name='all-friends'),
]
