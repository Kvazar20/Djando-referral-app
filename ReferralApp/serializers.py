from rest_framework import serializers
from .models import CustomUser
import re

class PhoneNumberSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

    def validate_phone(self, value):
        # Проверка номера телефона с использованием регулярного выражения
        phone_pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError("Неверный формат номера телефона.")
        return value

class VerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=4)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone', 'invite_code', 'activated_invite_code', 'referred_users']

    activated_invite_code = serializers.SerializerMethodField(method_name='get_activated_invite_code')
    referred_users = serializers.SerializerMethodField(method_name='get_referred_users')

    def get_referred_users(self, obj):
        # Получение списка номеров телефонов рефералов
        referred_users = obj.referred_users.all()
        return [user.phone for user in referred_users]

    def get_activated_invite_code(self, obj):
        # Если инвайт-код был активирован, вернуть инвайт-код активировавшего пользователя
        if obj.activated_invite_code:
            return obj.activated_invite_code.invite_code
        return None