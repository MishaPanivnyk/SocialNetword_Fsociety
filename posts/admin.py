from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'image_preview', 'description', 'likes', 'creation_date_time')
    search_fields = ['author__username', 'description']

    def image_preview(self, obj):
        return obj.image.url if obj.image else None
    image_preview.short_description = 'Image'

admin.site.register(Post, PostAdmin)
