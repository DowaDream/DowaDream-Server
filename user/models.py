from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # default: id, username, email, date_joined
    profile_img = models.ImageField(default=None)
    fighting = models.IntegerField(default=0)
    resol_msg = models.CharField(max_length=100, verbose_name="다짐메세지")
    
    # tags = models.ListCharField(
    #     base_field=models.CharField(max_length=15),
    #     size=10,
    #     max_length=(10 * 15),  # 15 * 10 characters, plus commas
    # )
    
    # regions = models.ListCharField(     # 시군구 코드
    #     base_field=models.CharField(max_length=15),
    #     size=10,
    #     max_length=(10 * 15),
    # )
    
    # cheered_progrms = models.ListCharField(
    #     base_field=models.CharField(max_length=10),
    #     size=50,
    #     max_length=(10 * 50),
    # )
    
    # clipped_progrms = models.ListCharField(
    #     base_field=models.CharField(max_length=10),
    #     size=50,
    #     max_length=(10 * 50),
    # )
    
    # my_progrms = models.ListCharField(
    #     base_field=models.CharField(max_length=10),
    #     size=50,
    #     max_length=(10 * 50),
    # )
    
    # cheered_reviews = models.ListCharField(
    #     base_field=models.CharField(max_length=10),
    #     size=50,
    #     max_length=(10 * 50),
    # )