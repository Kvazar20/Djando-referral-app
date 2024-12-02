from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import PhoneNumberSerializer, VerificationCodeSerializer, UserProfileSerializer
from .models import CustomUser
import random
import string
import time


@api_view(['POST'])
def enter_phone(request):
    serializer = PhoneNumberSerializer(data=request.data)
    if serializer.is_valid():
        phone = serializer.validated_data['phone']

        # Имитация задержки на сервере
        time.sleep(1)

        # Генерация случайного 4-значного кода
        verification_code = ''.join(random.choices(string.digits, k=4))

        # Сохраняем код и номер телефона в сессии
        request.session['verification_code'] = verification_code
        request.session['phone'] = phone

        # Отправляем код и выводим сообщение об успешной отправке
        return Response({'message': 'Код подтверждения отправлен успешно!', 'Verification code': verification_code},
                        status=status.HTTP_200_OK)


    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def enter_code(request):
    serializer = VerificationCodeSerializer(data=request.data)
    if serializer.is_valid():
        entered_code = serializer.validated_data['verification_code']

        # Получаем номер телефона и код из сессии
        phone = request.session.get('phone')
        stored_code = request.session.get('verification_code')

        # Проверяем наличие в сессии номера телефона и кода
        if not phone or not stored_code:
            return Response({'error': 'Код подтверждения не найден!'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем соответствие веденного кода
        if entered_code != stored_code:
            return Response({'error': 'Неверный код подтверждения!'}, status=status.HTTP_401_UNAUTHORIZED)

        # Авторизация пользователя
        user, created = CustomUser.objects.get_or_create(phone=phone)

        # Присваиваем пользователю токен
        token, created = Token.objects.get_or_create(user=user)

        # Очистка сессии
        request.session.flush()

        return Response({'message': 'Авторизация прошла успешно!', 'token': token.key}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    user_serializer = UserProfileSerializer(user)

    print(f"Activated Invite Code: {user.activated_invite_code}")

    if request.method == 'GET':
        return Response(user_serializer.data, status=status.HTTP_200_OK)


    elif request.method == 'POST':
        # Обработка ввода инвайт-кода
        invite_code = request.data.get('invite_code')

        # Проверка на наличие введенного инвайт-кода
        if not invite_code:
            return Response({'error': "Введите инвайт-код."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка на наличие активированного инвайт-кода
        elif user.activated_invite_code is not None:
            return Response({'error': "Вы уже активировали инвайт-код!"}, status=status.HTTP_409_CONFLICT)

        else:
            try:
                # Проверяем, существует ли пользователь с таким инвайт-кодом
                inviter = CustomUser.objects.get(invite_code=invite_code)
                user.activated_invite_code = inviter
                user.save()

                # Сообщение об успешном активировании инвайт-кода
                success_message = f"Инвайт-код {invite_code} успешно активирован!"
                return Response({'message': success_message}, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                error_message = "Пользователь с данным инвайт-кодом не найден!"
                return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)