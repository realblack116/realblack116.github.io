from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 사용자에게 확장 필드가 필요하면 여기에 추가하세요
    # 예: phone = models.CharField(max_length=20, blank=True)
    pass
