from django.db import models
from cloudinary.models import CloudinaryField
from account.models import CustomUser

class Story(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media = CloudinaryField('media', blank=True)  
    description = models.TextField(blank=True)
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Story by {self.author.name}'

class LikeStory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} likes {self.story.author.name}\'s story'
    
class CommentStory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.name} on {self.story.author.name}\'s story'
