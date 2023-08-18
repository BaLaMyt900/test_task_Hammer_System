from django.http import HttpRequest
from django.shortcuts import render
from .models import User
import random
import string
import time


def _generate_referal_code() -> str:
    """ Генератор реферального кода """
    letters_and_digits = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.sample(letters_and_digits, 6))
        """ Проверка на уникальность """
        if not User.objects.get(user_referal_code=code).exists():
            return code


def _send_sms(number: int) -> bool:
    """ Проверка номера отправкой смс кода. Возвращает истину если пройдена. """
    time.sleep(3)
    return True


def _strToInt(str) -> int:
    """ Функция, убирающая все знаки кроме цифр.
     Возвращает int"""
    result = ''
    for s in str:
        if s.isdigit():
            result += s
    return int(result)


def user_autorization(request: HttpRequest):
    """ Функция регистрации пользователя """
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        phone = _strToInt(request.POST['phone'])
        """ Отработка ошибок """
        if not phone:
            return render(request, 'index.html', {'error': 'Для продолжения, введите номер телефона.'})
        elif len(str(phone)) != 11 or str(phone)[0] != '7':
            return render(request, 'index.html', {'error': 'Введен неккоректный номер.', 'phone': phone})

        if _send_sms(phone):
            """ Если пройдена проверка номера """
            user = User.objects.get(phone=phone)
            if not user:
                """ Пользователь не найден. Регистрация. """
                user = User.objects.create(phone=phone, user_referral_code=_generate_referal_code())




        return render(request, 'index.html')
