from django.db import models
from cloudinary.models import CloudinaryField
from account.models import CustomUser

class Reel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = CloudinaryField('video', blank=True)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    creation_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class LikeReels(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.reel}"

class CommentReels(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reel = models.ForeignKey(Reel, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.reel}"
    
