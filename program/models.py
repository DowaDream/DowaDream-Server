from django.db import models
from user.models import User

CHOICES = [
    (True, 'True'),
    (False, 'False')
]

class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성 일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정 일시", auto_now=True)

    class Meta:
        abstract = True


class Program_Interaction(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, verbose_name="사용자")
    progrmRegistNo = models.CharField(max_length=20, verbose_name="봉사 등록번호")
    cheered = models.BooleanField(choices=CHOICES, default=False, verbose_name="봉사 응원 여부")
    participated = models.BooleanField(choices=CHOICES, default=False, verbose_name="봉사 참여 여부")
    clipped = models.BooleanField(choices=CHOICES, default=False, verbose_name="봉사 스크랩 여부")