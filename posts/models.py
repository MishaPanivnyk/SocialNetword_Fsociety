from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True)  
    description = models.TextField()
    likes = models.IntegerField(default=0)
    creation_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    