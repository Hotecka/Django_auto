from django.db import models
from users.models import User


class Car(models.Model):
    # Поле для хранения марки автомобиля
    make = models.CharField(
        max_length=30,
        verbose_name="Марка", 
    )
    
    # Поле для хранения модели автомобиля
    model = models.CharField(
        max_length=50,
        verbose_name="Модель", 
    )
    
    # Поле для хранения года выпуска автомобиля
    year = models.PositiveIntegerField(
        verbose_name="Год выпуска",  
    )
    
    # Поле для хранения описания автомобиля (необязательное)
    description = models.TextField(
        blank=True,  # Поле может быть пустым
        null=True,   # Поле может быть пустым в базе данных
        verbose_name="Описание",  
    )
    
    # Поле для хранения даты и времени создания записи
    created_at = models.DateTimeField(
        auto_now_add=True,  # Дата автоматически устанавливается при создании записи
    )
    
    # Поле для хранения даты и времени последнего обновления записи
    updated_at = models.DateTimeField(
        auto_now=True,  # Дата автоматически обновляется при изменении записи
    )
    
    # Связь с пользователем (владельцем машины)
    owner = models.ForeignKey(
        User,  # Ссылаемся на модель пользователя
        on_delete=models.CASCADE,  # При удалении пользователя удаляются все связанные машины
    )

    class Meta:
        db_table = "car"  # Имя таблицы в базе данных
        verbose_name = "Car"  
        verbose_name_plural = "Cars"  

    def __str__(self):
        # Представление строки объекта
        return f"{self.make} {self.model} {self.year}"


class Comment(models.Model):
    # Поле для хранения содержания комментария
    content = models.CharField(
        verbose_name="Содержимое комментария", 
    )
    
    # Поле для хранения даты и времени создания комментария
    created_at = models.DateTimeField(
        auto_now_add=True,  # Дата автоматически устанавливается при создании комментария
    )
    
    # Связь с машиной, к которой относится комментарий
    car = models.ForeignKey(
        Car,  # Ссылаемся на модель автомобиля
        on_delete=models.CASCADE,  # При удалении автомобиля удаляются все связанные комментарии
    )
    
    # Связь с автором комментария (пользователем)
    author = models.ForeignKey(
        User,  # Ссылаемся на модель пользователя (автора комментария)
        on_delete=models.CASCADE,  # При удалении пользователя удаляются все его комментарии
    )

    class Meta:
        db_table = "comment"  # Имя таблицы в базе данных
        verbose_name = "Comment" 
        verbose_name_plural = "Comments"  

    def __str__(self):
        # Представление строки объекта
        return f"От {self.author} о {self.car}"
