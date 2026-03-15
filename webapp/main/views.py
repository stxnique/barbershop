from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Appointment, Profile
import re


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        errors = []

        if not name:
            errors.append('Укажите имя')
        elif not re.match(r'^[а-яА-Яa-zA-Z\s\-]+$', name):
            errors.append('Имя должно содержать только буквы, пробелы и дефисы')

        if phone:
            clean_phone = re.sub(r'[^\d+]', '', phone)
            if not re.match(r'^\+?\d+$', clean_phone):
                errors.append('Телефон должен содержать только цифры и может начинаться с +')
            else:
                phone = clean_phone

        if not email:
            errors.append('Укажите email')

        if not message:
            errors.append('Напишите сообщение')

        if not errors:
            Appointment.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message
            )
            messages.success(request, 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')

        for error in errors:
            messages.error(request, error)

        return render(request, 'main/contacts.html', {
            'form_data': {
                'name': name,
                'phone': phone,
                'email': email,
                'message': message,
            }
        })

    return render(request, 'main/contacts.html')


def services(request):
    return render(request, 'main/services.html')


def barbers(request):
    return render(request, 'main/barbers.html')


def user_login(request):
    """Вход по номеру телефона или имени пользователя"""
    if request.method == 'POST':
        login_input = request.POST.get('login_input', '').strip()  # может быть телефон или имя
        password = request.POST.get('password', '').strip()

        user = None

        # Пытаемся найти пользователя по телефону
        try:
            # Очищаем телефон от лишних символов
            clean_phone = re.sub(r'[^\d+]', '', login_input)
            profile = Profile.objects.get(phone=clean_phone)
            user = profile.user
        except Profile.DoesNotExist:
            # Если не нашли по телефону, пробуем по имени пользователя
            try:
                user = User.objects.get(username=login_input)
            except User.DoesNotExist:
                user = None

        if user is not None:
            # Проверяем пароль
            if user.check_password(password):
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('index')
            else:
                messages.error(request, 'Неверный пароль')
        else:
            messages.error(request, 'Пользователь с таким телефоном или именем не найден')

        return render(request, 'main/login.html', {
            'login_input': login_input
        })

    return render(request, 'main/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')


def user_register(request):
    """Регистрация нового пользователя с телефоном"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        errors = []

        # Проверка имени пользователя
        if not username:
            errors.append('Введите имя пользователя')
        elif len(username) < 3:
            errors.append('Имя пользователя должно быть не менее 3 символов')
        elif User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким именем уже существует')

        # Проверка телефона
        if not phone:
            errors.append('Введите номер телефона')
        else:
            # Очищаем телефон от лишних символов
            clean_phone = re.sub(r'[^\d+]', '', phone)
            if not re.match(r'^\+?\d{10,15}$', clean_phone):
                errors.append('Введите корректный номер телефона (10-15 цифр)')
            elif Profile.objects.filter(phone=clean_phone).exists():
                errors.append('Пользователь с таким телефоном уже существует')
            else:
                phone = clean_phone

        # Проверка email
        if not email:
            errors.append('Введите email')
        elif User.objects.filter(email=email).exists():
            errors.append('Пользователь с таким email уже существует')

        # Проверка пароля
        if not password1:
            errors.append('Введите пароль')
        elif len(password1) < 6:
            errors.append('Пароль должен быть не менее 6 символов')

        if password1 != password2:
            errors.append('Пароли не совпадают')

        if not errors:
            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            # Создаем профиль с телефоном
            Profile.objects.create(
                user=user,
                phone=phone
            )

            # Сразу авторизуем пользователя
            login(request, user)

            messages.success(request, f'Добро пожаловать, {username}! Регистрация прошла успешно.')
            return redirect('index')

        for error in errors:
            messages.error(request, error)

        return render(request, 'main/register.html', {
            'form_data': {
                'username': username,
                'phone': phone,
                'email': email,
            }
        })

    return render(request, 'main/register.html')