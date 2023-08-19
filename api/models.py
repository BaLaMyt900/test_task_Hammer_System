from django.contrib.auth.models import AbstractUser
from django.db import models


class User(models.Model):
    """ Модель пользователя согласно тех. заданию"""
    phone = models.IntegerField(unique=True, null=True)
    user_referral_code = models.CharField(unique=True, max_length=6)
    referral_code = models.CharField(null=True, blank=True, max_length=6)


class UserReferrals(models.Model):
    """ Модель связи пользователей и рефералов """
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    referral = models.ForeignKey(User, related_name='referral', to_field='user_referral_code', on_delete=models.CASCADE)