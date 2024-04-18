from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from account.models import CustomUser

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True)  
    description = models.TextField()
    likes = models.IntegerField(default=0)
    creation_date_time = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Comment', related_name='comments', blank=True)

    def __str__(self):
        return self.description

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    isLike = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.post}"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
