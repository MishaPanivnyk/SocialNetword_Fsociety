from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
import os
from django.conf import settings
from cloudinary.models import CloudinaryField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    confirmPassword = models.CharField(max_length=255)
    avatar = CloudinaryField('image', default='default_avatar.jpg')
    bio = models.TextField(max_length=20,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    located = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 
    is_email_verified = models.BooleanField(default=False) 
    account_token = models.CharField(max_length=255, blank=True, null=True) 
    friends_count = models.IntegerField(default=0)
    subscribers_count = models.IntegerField(default=0)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_email_verification_token(self):
        return default_token_generator.make_token(self)

    def get_email_verification_url(self, request):
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = self.get_email_verification_token()
        return request.build_absolute_uri('/')[:-1] + reverse('verify_email', kwargs={'uidb64': uidb64, 'token': token})


    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff