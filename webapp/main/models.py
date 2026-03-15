from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    """Модель для записи на стрижку"""
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"


class Profile(models.Model):
    """Модель профиля пользователя для хранения телефона"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    phone = models.CharField(
        'Телефон',
        max_length=20,
        unique=True,
        help_text='Номер телефона в формате +79991234567'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.phone}"