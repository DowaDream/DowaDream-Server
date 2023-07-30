from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 기본 제공: username, first_name, last_name, email, date_joined
    category = models.CharField(verbose_name="카테고리", null=True, max_length=150) # 나중에 여러 개로 수정필요
    region = models.CharField(verbose_name="지역", null=True, max_length=150)   # 시군구 코드
    age = models.IntegerField(verbose_name="나이", null=True)