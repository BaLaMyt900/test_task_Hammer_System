from django.contrib.auth.models import AbstractUser
from django.db import models
import string
import random


def _generate_referal_code() -> str:
    """ Генератор реферального кода """
    letters_and_digits = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.sample(letters_and_digits, 6))
        """ Проверка на уникальность """
        if not User.objects.get(referal_code=code).exists():
            return code


class User(AbstractUser):
    """ Расширенная модель стандарного django пользователя
     согласно тех. заданию"""
    phone = models.IntegerField(unique=True, null=False)
    referral_code = models.CharField(unique=True, max_length=6, default=_generate_referal_code())
    user_referral_code = models.CharField(null=True, blank=True)

