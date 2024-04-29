from django.contrib import admin
from .models import Post, Like, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'image_preview', 'description', 'likes', 'creation_date_time')  # Додайте 'id' до list_display
    search_fields = ['id', 'author__username', 'description']  # Додайте 'id' до search_fields

    def image_preview(self, obj):
        return obj.image.url if obj.image else None
    image_preview.short_description = 'Image'

admin.site.register(Post, PostAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ['user__username', 'post__description']

admin.site.register(Like, LikeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'post', 'text', 'created_at')
    search_fields = ['user__username', 'post__description', 'text']

admin.site.register(Comment, CommentAdmin)
