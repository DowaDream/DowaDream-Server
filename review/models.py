from django.db import models
from user.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성 일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정 일시", auto_now=True)

    class Meta:
        abstract = True

# is_public 필드의 choices 정의
IS_PUBLIC_CHOICES = [
    (True, 'True'),
    (False, 'False')
]

class Review(BaseModel):
    # 자동으로 들어가는 필드
    rid = models.AutoField(primary_key=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    
    progrmRegistNo = models.CharField(max_length=20, verbose_name="봉사 등록번호")
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_public = models.BooleanField(choices=IS_PUBLIC_CHOICES, default=True)
    category = models.CharField(max_length=60, verbose_name="봉사 태그")
    region = models.CharField(max_length=30, verbose_name="봉사 지역")
    actPlace = models.CharField(max_length=60, verbose_name="봉사 장소")


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(verbose_name="리뷰 이미지")
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return str(self.image)


class Comment(BaseModel):
    cid = models.AutoField(primary_key=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    content = models.TextField(verbose_name="댓글 텍스트", blank=False)
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)


class Cheered_Review(BaseModel):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)