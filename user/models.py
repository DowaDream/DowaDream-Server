from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # default: id, username, email, date_joined
    profile_img = models.ImageField(default=None, verbose_name="구글 프로필 이미지")
    fighting = models.IntegerField(default=0, verbose_name="파이팅 지수")
    resol_msg = models.CharField(max_length=100, verbose_name="다짐 메세지")

class User_Tag(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, verbose_name="유저")
    tag = models.CharField(max_length=10, verbose_name="봉사분야코드")

class User_Region(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, verbose_name="유저")
    region = models.CharField(max_length=20, verbose_name="시군구 코드")