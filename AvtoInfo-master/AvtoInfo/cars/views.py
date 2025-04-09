from typing import TYPE_CHECKING

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from cars.models import Car, Comment
from cars.forms import CarForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def get_cars(request: "HttpRequest") -> "HttpResponse":
    """
    Представление для получения всех машин
    """

    queryset = Car.objects.order_by("id")

    context: dict = {
        "title": "Cars - Home",
        "cars": queryset,
    }
    return render(request, "cars/cars.html", context)


@login_required
def add_car(request: "HttpRequest") -> "HttpResponse":
    """
    Представление для добавления новой машины
    """

    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect(reverse("users:profile"))
    else:
        form = CarForm()

    context = {
        "title": "Добавить машину",
        "form": form,
    }

    return render(request, "cars/add_car.html", context)


def car_detail(request, car_id):
    """
    Представление с информацией о конкретном автомобиле и комментариями, а также форма для добавления комментариев
    """

    car = get_object_or_404(Car, id=car_id)
    comments = Comment.objects.filter(car=car)

    if request.method == "POST":
        content = request.POST.get("content")

        if not request.user.is_authenticated:
            return redirect("users:login")

        Comment.objects.create(
            content=content,
            car=car,
            author=request.user,
        )

        return HttpResponseRedirect(reverse("cars:car_detail", args=[car_id]))

    context = {
        "car": car,
        "comments": comments,
    }

    return render(request, "cars/car_detail.html", context)


@login_required
def edit_car(request, car_id):
    """
    Представление для изменеия данных о машине
    """

    car = get_object_or_404(
        Car,
        id=car_id,
        owner=request.user,
    )

    if request.method == "POST":
        car.make = request.POST.get("make")
        car.model = request.POST.get("model")
        car.year = request.POST.get("year")
        car.description = request.POST.get("description")
        car.save()
        return redirect(reverse("users:profile"))

    context = {
        "car": car,
    }

    return render(request, "cars/edit_car.html", context)


@login_required
def delete_car(request, car_id):
    """
    Представление для удаления машины
    """
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    car.delete()
    return redirect(reverse("users:profile"))
