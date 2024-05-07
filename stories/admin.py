from django.contrib import admin
from .models import Story, LikeStory, CommentStory

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'media_preview', 'created_at')
    search_fields = ['id', 'author__username']

    def media_preview(self, obj):
        return obj.media.url if obj.media else None
    media_preview.short_description = 'Media'

admin.site.register(Story, StoryAdmin)

class LikeStoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'created_at')
    search_fields = ['user__username', 'story__id']

admin.site.register(LikeStory, LikeStoryAdmin)

class CommentStoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'story', 'text', 'created_at')
    search_fields = ['user__username', 'story__id', 'text']

admin.site.register(CommentStory, CommentStoryAdmin)
