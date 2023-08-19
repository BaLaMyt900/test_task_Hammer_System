from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователя согласно тех. заданию"""
    phone = models.IntegerField(unique=True, null=True)
    user_referral_code = models.CharField(unique=True, max_length=6)
    referral_code = models.CharField(null=True, blank=True, max_length=6)
