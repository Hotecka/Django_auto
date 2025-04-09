from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth

from users.forms import (
    UserLoginForm,
    UserRegistrationForm,
    UserProfileForm,
)
from cars.models import Car

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


def login(request: "HttpRequest") -> "HttpResponse":
    """
    Представление для авторизации пользователя.
    Проверяет данные формы, а затем аутентифицирует пользователя.
    Перенаправляет на страницу списка машин в случае успеха.
    """

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)  # Аутентификация пользователя
                return HttpResponseRedirect(reverse("cars:home"))  # Перенаправление на главную страницу машин
            else:
                form.add_error(None, "Неверный логин или пароль")  # Ошибка при неверном логине или пароле
    else:
        form = UserLoginForm()  # Создаём пустую форму, если запрос GET

    context = {
        "title": "AvtoInfo - Authentication",  # Заголовок страницы
        "form": form,  # Передаем форму в контекст
    }

    return render(request, "users/login.html", context)


def registration(request: "HttpRequest") -> "HttpResponse":
    """
    Представление для регистрации нового пользователя.
    После успешной регистрации автоматически авторизует пользователя и перенаправляет на его профиль.
    """

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()  # Сохраняем нового пользователя

            user = form.instance  # Получаем зарегистрированного пользователя
            auth.login(request, user)  # Авторизуем пользователя

            return HttpResponseRedirect(reverse("users:profile"))  # Перенаправление на профиль пользователя
    else:
        form = UserRegistrationForm()  # Создаём пустую форму для регистрации

    context = {
        "title": "AvtoInfo - Registration",  # Заголовок страницы
        "form": form,  # Передаем форму в контекст
    }

    return render(request, "users/registration.html", context)


@login_required
def profile(request: "HttpRequest") -> "HttpResponse":
    """
    Представление профиля пользователя.
    Показывает информацию о пользователе и его машины, а также форму для редактирования профиля.
    """

    user_cars = Car.objects.filter(owner=request.user)  # Получаем все машины пользователя
    if request.method == "POST":
        form = UserProfileForm(
            data=request.POST,
            instance=request.user,  # Заполняем форму данными текущего пользователя
        )

        if form.is_valid():
            form.save()  # Сохраняем обновления профиля

            return HttpResponseRedirect(reverse("users:profile"))  # Перенаправление на профиль после сохранения

    else:
        form = UserProfileForm(instance=request.user)  # Создаем форму с текущими данными пользователя

    context = {
        "title": "AvtoInfo - Profile",  # Заголовок страницы
        "user_cars": user_cars,  # Список машин пользователя
        "form": form,  # Форма редактирования профиля
    }

    return render(request, "users/profile.html", context)


@login_required
def logout(request: "HttpRequest") -> "HttpResponse":
    """
    Представление для выхода пользователя из системы.
    Завершается выходом и перенаправлением на страницу входа.
    """
    auth.logout(request)  # Выход пользователя из системы
    return redirect(reverse("users:login"))  # Перенаправление на страницу входа
