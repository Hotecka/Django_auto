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
    Представление для получения всех машин.
    Отображает список всех автомобилей, отсортированных по ID.
    """

    queryset = Car.objects.order_by("id")  # Получаем все автомобили, отсортированные по ID

    context: dict = {
        "title": "Cars - Home",  # Название страницы
        "cars": queryset,  # Список машин для отображения в шаблоне
    }
    return render(request, "cars/cars.html", context)


@login_required
def add_car(request: "HttpRequest") -> "HttpResponse":
    """
    Представление для добавления новой машины.
    Только для аутентифицированных пользователей. 
    Создаёт машину с привязкой к текущему пользователю как владельцу.
    """

    if request.method == "POST":
        form = CarForm(request.POST)  # Получаем данные формы из POST-запроса
        if form.is_valid():
            car = form.save(commit=False)  # Создаём объект машины, но не сохраняем его сразу
            car.owner = request.user  # Привязываем владельца
            car.save()  # Сохраняем машину в базе данных
            return redirect(reverse("users:profile"))  # Перенаправляем на профиль пользователя
    else:
        form = CarForm()  # Если запрос GET, создаём пустую форму

    context = {
        "title": "Добавить машину",  # Заголовок страницы
        "form": form,  # Передаем форму в контекст для отображения
    }

    return render(request, "cars/add_car.html", context)


def car_detail(request, car_id):
    """
    Представление с информацией о конкретном автомобиле и комментариями,
    а также форма для добавления комментариев.
    """

    car = get_object_or_404(Car, id=car_id)  # Получаем объект машины по ID, если нет — 404 ошибка
    comments = Comment.objects.filter(car=car)  # Получаем все комментарии для этой машины

    if request.method == "POST":
        content = request.POST.get("content")  # Получаем текст комментария из формы

        if not request.user.is_authenticated:
            return redirect("users:login")  # Если пользователь не авторизован, перенаправляем на страницу логина

        Comment.objects.create(  # Создаём новый комментарий
            content=content,
            car=car,  # Привязываем комментарий к машине
            author=request.user,  # Устанавливаем автора комментария
        )

        return HttpResponseRedirect(reverse("cars:car_detail", args=[car_id]))  # Перенаправляем на текущую страницу машины

    context = {
        "car": car,  # Передаем машину в контекст для отображения
        "comments": comments,  # Передаем комментарии для отображения
    }

    return render(request, "cars/car_detail.html", context)


@login_required
def edit_car(request, car_id):
    """
    Представление для изменения данных о машине.
    Позволяет владельцу машины изменять её данные.
    """

    car = get_object_or_404(  # Получаем объект машины по ID и проверяем, что владелец — текущий пользователь
        Car,
        id=car_id,
        owner=request.user,  # Только если текущий пользователь является владельцем
    )

    if request.method == "POST":
        car.make = request.POST.get("make")  # Обновляем марку машины
        car.model = request.POST.get("model")  # Обновляем модель машины
        car.year = request.POST.get("year")  # Обновляем год выпуска
        car.description = request.POST.get("description")  # Обновляем описание
        car.save()  # Сохраняем изменения
        return redirect(reverse("users:profile"))  # Перенаправляем на страницу профиля пользователя

    context = {
        "car": car,  # Передаем машину для редактирования в контекст
    }

    return render(request, "cars/edit_car.html", context)


@login_required
def delete_car(request, car_id):
    """
    Представление для удаления машины.
    Удаляет машину, если текущий пользователь — её владелец.
    """

    car = get_object_or_404(Car, id=car_id, owner=request.user)  # Получаем объект машины, только если текущий пользователь — её владелец
    car.delete()  # Удаляем машину из базы данных
    return redirect(reverse("users:profile"))  # Перенаправляем на профиль пользователя
