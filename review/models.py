from django.db import models
from user.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성 일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정 일시", auto_now=True)

    class Meta:
        abstract = True


class Review(BaseModel):
    rid = models.AutoField(primary_key=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    content = models.TextField(verbose_name="리뷰 텍스트")
    progrmRegistNo = models.CharField(max_length=15, verbose_name="봉사 등록번호")  # 1266114
    category = models.CharField(max_length=60, verbose_name="봉사 카테고리")    # 생활편의지원 > 이동지원

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(verbose_name="리뷰 이미지")
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return str(self.image)