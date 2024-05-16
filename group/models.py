from django.db import models
from cloudinary.models import CloudinaryField
from account.models import CustomUser

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)
    image = CloudinaryField('image', blank=True) 
    header_image  = CloudinaryField('header_image', blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)  
    location = models.CharField(max_length=100, blank=True, null=True)  

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(CustomUser, related_name='group_memberships')

    post_count = models.IntegerField(default=0) 
    total_likes = models.IntegerField(default=0) 

    is_staff = models.BooleanField(default=False) 
    is_follow = models.BooleanField(default=False)

class GroupMembership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)