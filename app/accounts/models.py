from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import ChatUserManager


class ChatUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, max_length=40, unique=True)
    email = models.EmailField()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_online = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)

    social_media = models.URLField()
    # profile_image = models.ImageField(verbose_name='profile image')

    USERNAME_FIELD = 'id'
    EMAIL_FIELD = 'email'

    objects = ChatUserManager()

    def __str__(self):
        return self.id
