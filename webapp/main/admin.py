from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Appointment, Profile


class ProfileInline(admin.StackedInline):
    """Встраиваемая форма для профиля в админке пользователя"""
    model = Profile
    can_delete = False
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'
    fields = ['phone', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class CustomUserAdmin(UserAdmin):
    """Кастомный админ для пользователей с профилем"""
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_phone', 'is_staff']
    list_select_related = ['profile']

    def get_phone(self, obj):
        """Получить телефон из профиля"""
        try:
            return obj.profile.phone
        except Profile.DoesNotExist:
            return '-'

    get_phone.short_description = 'Телефон'
    get_phone.admin_order_field = 'profile__phone'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Админка для записей на стрижку"""
    list_display = ['name', 'email', 'phone', 'created_at', 'short_message']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    def short_message(self, obj):
        """Сокращенное сообщение"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message

    short_message.short_description = 'Сообщение'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админка для профилей пользователей"""
    list_display = ['user', 'phone', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Контактные данные', {
            'fields': ('phone',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Перерегистрируем модель User с кастомным админом
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)