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

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("cars:home"))
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = UserLoginForm()

    context = {
        "title": "AvtoInfo - Authentication",
        "form": form,
    }

    return render(request, "users/login.html", context)


def registration(request: "HttpRequest") -> "HttpResponse":

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()

            user = form.instance
            auth.login(request, user)

            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "AvtoInfo - Registration",
        "form": form,
    }

    return render(request, "users/registration.html", context)


@login_required
def profile(request: "HttpRequest") -> "HttpResponse":

    user_cars = Car.objects.filter(owner=request.user)
    if request.method == "POST":
        form = UserProfileForm(
            data=request.POST,
            instance=request.user,
        )

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("users:profile"))

    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "title": "AvtoInfo - Profile",
        "user_cars": user_cars,
        "form": form,
    }

    return render(request, "users/profile.html", context)


@login_required
def logout(request: "HttpRequest") -> "HttpResponse":
    auth.logout(request)
    return redirect(reverse("users:login"))
