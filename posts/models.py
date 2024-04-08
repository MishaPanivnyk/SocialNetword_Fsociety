from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')  
    description = models.TextField()
    likes = models.IntegerField(default=0)
    creation_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description