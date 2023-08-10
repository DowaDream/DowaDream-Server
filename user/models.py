from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # default: id, username, email, date_joined
    profile_img = models.ImageField(default=None)
    fighting = models.IntegerField(default=0)
    resol_msg = models.CharField(max_length=100, verbose_name="다짐메세지")