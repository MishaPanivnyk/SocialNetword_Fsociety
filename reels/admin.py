from django.contrib import admin
from .models import Reel, LikeReels, CommentReels

class ReelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'video_preview', 'description', 'likes', 'creation_date_time')
    search_fields = ['id', 'author__username', 'description']

    def video_preview(self, obj):
        return obj.video.url if obj.video else None
    video_preview.short_description = 'Video'

admin.site.register(Reel, ReelAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'reel')
    search_fields = ['user__username', 'reel__description']

admin.site.register(LikeReels, LikeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reel', 'text', 'created_at')
    search_fields = ['user__username', 'reel__description', 'text']

admin.site.register(CommentReels, CommentAdmin)