from django.urls import path
from .views import StoryView

story_view = StoryView()

urlpatterns = [
    path('stories_create/', story_view.create_story, name='create_story'),
    path('stories_like/', story_view.like_story, name='like_story'),
    path('stories_comment/', story_view.comment_story, name='comment_story'),
    path('stories_delete_comment/', story_view.delete_comment, name='delete_comment_story'),
    path('stories_unlike/', story_view.unlike_story, name='unlike_story'),
    path('stories_user/<str:author_identifier>/', story_view.look_story_list_user, name='look_story_list_user'),
    path('stories_all/', story_view.look_story_list_all, name='look_story_list_all'),
    path('reels_check/', story_view.delete_old_stories, name='delete_old_stories'),
    path('reels_delete/', story_view.delete_own_story, name='delete_own_story'),
]
