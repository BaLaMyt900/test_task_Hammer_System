import random
import string
import time
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, UserReferrals


def _generatator(type: int) -> str:
    """ Генератор """
    letters_and_digits = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.sample(letters_and_digits, 6))
        """ Проверка на уникальность """
        try:
            if type == 1:
                User.objects.get(user_referral_code=code)
            elif type == 2:
                User.objects.get(username=code)
            elif type == 3:
                User.objects.get(password=code)
        except User.DoesNotExist:
            return code


def _strToInt(str) -> int:
    """ Функция, убирающая все знаки кроме цифр.
     Возвращает int"""
    result = ''
    for s in str:
        if s.isdigit():
            result += s
    return int(result)


def _send_sms(number: int) -> bool:
    """ Проверка номера отправкой смс кода. Возвращает истину если смс отправлено. """
    time.sleep(2)
    return True


class StartPage(APIView):
    """ Стартовая страница """
    def get(self, request: Request) -> Response:
        if 'phone' in request.session:
            try:
                user = User.objects.get(phone=request.session['phone'])
            except User.DoesNotExist:
                pass
            else:
                connected_referrals = UserReferrals.objects.filter(referral=user).values('user__phone')
                profile = {'phone': user.phone, 'user_referral_code': user.user_referral_code,
                           'referral_code': user.referral_code, 'connected_referrals': connected_referrals}
                return Response({'status': 1, 'message': 'Добрый день!', 'profile': profile})
        return Response({'status': 1, 'message': 'Добрый день. Для продолжения напишите в запросе Вам телефон.'})

    def post(self, request: Request) -> Response:
        if 'phone' in request.POST:
            """ Получен телефон пользователя """
            phone = _strToInt(request.POST['phone'])
            """ Отработка ошибок """
            if not phone:
                return Response({'status': 1, 'error': 'Для продолжения, введите номер телефона.'})
            elif len(str(phone)) != 11 or str(phone)[0] != '7':
                return Response({'status': 1, 'error': 'Введен неккоректный номер.', 'phone': phone})

            """ Записываем телефон пользователя в сессию """
            request.session['phone'] = phone
            if _send_sms(phone):
                return Response({'status': 1,
                                 'message': 'На Ваш номер отправлено смс сообщение подтверждения телефона, Введите код.'})
        elif 'sms-code' in request.POST:
            ''' Пользователь ввел код '''
            if int(request.POST['sms-code']) == 0000 and request.session['phone']:
                try:
                    user = User.objects.get(phone=request.session['phone'])
                except User.DoesNotExist:
                    user = User.objects.create(username=_generatator(2), password=_generatator(3),
                                               phone=request.session['phone'], user_referral_code=_generatator(1))
                    profile = {'phone': user.phone, 'user_referral_code': user.user_referral_code}
                    return Response({'status': 1, 'message': 'Регистрация завершена.', 'profile': profile})
                else:
                    profile = {'phone': user.phone, 'user_referral_code': user.user_referral_code,
                               'referral_code': user.referral_code}
                    return Response({'status': 1, 'message': 'Добрый день!', 'profile': profile})
            else:
                return Response({'status': 0, 'message': 'Не правильный смс код.'})
        else:
            return Response({'status': 0})


class EnterReferralCode(APIView):
    """ Логика введения чужого реферального кода. """
    def post(self, request: Request):
        if 'referral_code' in request.POST and 'phone' in request.session:
            try:
                user = User.objects.get(phone=request.session['phone'])
            except User.DoesNotExist:
                return Response({'status': 0,
                                 'error': 'Ваш телефон не найден. Зарегерстрируйтесь или авторизуйтесь снова.'})
            else:
                try:
                    referral = User.objects.get(user_referral_code=request.POST['referral_code'])
                except User.DoesNotExist:
                    return Response({'status': 0, 'message': 'Реферальный код не найден.'})
                else:
                    UserReferrals.objects.create(user=user, referral=referral)
                    user.referral_code = request.POST['referral_code']
                    user.save()
                    return Response({'status': 1, 'message': 'Реферальный код принят.'})
