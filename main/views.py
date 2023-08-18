from django.shortcuts import render
from .models import User
import random
import string


def generate_referal_code() -> str:
    """ Генератор реферального кода """
    letters_and_digits = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.sample(letters_and_digits, 6))
        """ Проверка на уникальность """
        if not User.objects.get(user_referal_code=code).exists():
            return code



