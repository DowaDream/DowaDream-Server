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
    rid = models.AutoField(primary_key=True, verbose_name="봉사 ID")
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, verbose_name="작성자")
    
    progrmRegistNo = models.CharField(max_length=20, verbose_name="봉사 등록번호")
    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    is_public = models.BooleanField(choices=IS_PUBLIC_CHOICES, default=True, verbose_name="공개 여부(공개면 True)")
    # tag = models.CharField(max_length=60, verbose_name="봉사 태그")
    # region = models.CharField(max_length=30, verbose_name="봉사 지역(시군구 코드)")
    # actPlace = models.CharField(max_length=60, verbose_name="봉사 장소")


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(verbose_name="리뷰 이미지")
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return str(self.image)


class Comment(BaseModel):
    cid = models.AutoField(primary_key=True, verbose_name="댓글 ID")
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, verbose_name="댓글 작성자")
    content = models.TextField(blank=False, verbose_name="댓글 내용")
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)


class Cheered_Review(BaseModel):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)