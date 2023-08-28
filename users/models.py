from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='E-mail', unique=True)
    tg_user_name = models.CharField(max_length=150, verbose_name='username в ТГ', **NULLABLE)
    tg_user_id = models.CharField(max_length=150, verbose_name='user_id в ТГ', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.tg_user_name
