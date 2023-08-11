from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # default: id, username, email, date_joined
    profile_img = models.ImageField(default=None, verbose_name="구글 프로필 이미지")
    fighting = models.IntegerField(default=0, verbose_name="파이팅 지수")
    resol_msg = models.CharField(max_length=100, verbose_name="다짐 메세지")