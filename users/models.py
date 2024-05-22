from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message='Телефон должен содержать от 9 до 15 цифр')


class User(AbstractUser):
    username = None
    # Регистрация по номеру телефона
    telephone = models.CharField(max_length=20, validators=[phone_regex], verbose_name='Телефон', unique=True)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email', unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    # company = models.CharField(max_length=20, verbose_name='Компания')
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name}, {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
