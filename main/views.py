from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login
from django.http import HttpResponseNotFound
from .models import User
import random
import string
import time


def _generate_referral_code() -> str:
    """ Генератор реферального кода """
    letters_and_digits = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.sample(letters_and_digits, 6))
        """ Проверка на уникальность """
        try:
            User.objects.get(user_referral_code=code)
        except User.DoesNotExist:
            return code


def _send_sms(number: int, code: int) -> bool:
    """ Проверка номера отправкой смс кода. Возвращает истину если пройдена. """
    time.sleep(2)
    if code == 0000:
        return True
    else:
        return False


def _strToInt(str) -> int:
    """ Функция, убирающая все знаки кроме цифр.
     Возвращает int"""
    result = ''
    for s in str:
        if s.isdigit():
            result += s
    return int(result)


class Registration(CreateView):
    """ Страница регистрации пользователя """
    model = User
    template_name = 'registration.html'
    success_url = '/profile/'
    fields = ['username', 'password', 'phone']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'phone' in self.args:
            print(self.args)
        if 'phone' in context:
            print('context')
            print(context)
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_referral_code = _generate_referral_code()
        user.save()
        login(self.request, user)
        return redirect('/profile/')


class Profile(DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        """ Автоматическое добавление аргумента PK если авторизованный пользователь заходит на свой профиль """
        if self.request.user.is_authenticated:
            self.kwargs['pk'] = self.request.user.pk
            return super().get_object(queryset)
        else:
            return HttpResponseNotFound()


def index(request: HttpRequest):
    """ Авторизация пользователя, переадресация на регистрацию при первом входе """
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        phone = _strToInt(request.POST['phone'])
        """ Отработка ошибок """
        if not phone:
            return render(request, 'index.html', {'error': 'Для продолжения, введите номер телефона.'})
        elif len(str(phone)) != 11 or str(phone)[0] != '7':
            return render(request, 'index.html', {'error': 'Введен неккоректный номер.', 'phone': phone})
        code = _strToInt(request.POST['sms-code'])
        if _send_sms(phone, code):
            """ Если пройдена проверка номера """
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                return render(request, 'registration.html', {'phone': phone})
            else:
                login(request, user)
                return redirect('profile/')
        else:
            return HttpResponseNotFound('Неверный смс код')
