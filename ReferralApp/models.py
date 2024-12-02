from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import random
import string

# Модель пользователя
class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)  # Номер телефона
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)  # Инвайт-код пользователя
    activated_invite_code = models.ForeignKey(  # Активированный инвайт-код
        'self',
        null=True,
        blank=True,
        related_name='referred_users',
        on_delete=models.SET_NULL
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if not self.invite_code:  # Генерация инвайт-кода при создании
            self.invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super().save(*args, **kwargs)
