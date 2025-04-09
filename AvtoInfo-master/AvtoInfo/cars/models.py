from django.db import models
from users.models import User


class Car(models.Model):
    make = models.CharField(
        max_length=30,
        verbose_name="Марка",
    )
    model = models.CharField(
        max_length=50,
        verbose_name="Модель",
    )
    year = models.PositiveIntegerField(
        verbose_name="Год выпуска",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table: str = "car"
        verbose_name: str = "Car"
        verbose_name_plural: str = "Cars"

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"


class Comment(models.Model):
    content = models.CharField(
        verbose_name="Содержимое комментария",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table: str = "comment"
        verbose_name: str = "Comment"
        verbose_name_plural: str = "Comments"

    def __str__(self):
        return f"От {self.author} о {self.car}"
