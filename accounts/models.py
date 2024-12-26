from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    birthday = models.DateField()
    gender = models.CharField(
        max_length=10, blank=True, null=True)  # 'male', 'female' 등
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username