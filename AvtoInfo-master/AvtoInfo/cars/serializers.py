from rest_framework import serializers
from cars.models import Car, Comment

class CarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Car.
    Преобразует объекты модели Car в формат JSON и наоборот для использования в API.
    """

    class Meta:
        model = Car  # Указываем модель, для которой создается сериализатор
        fields = [
            "id",          # Идентификатор машины
            "make",        # Марка машины
            "model",       # Модель машины
            "year",        # Год выпуска машины
            "description", # Описание машины
            "owner",       # Владелец машины (связан с пользователем)
            "created_at",  # Дата создания записи о машине
            "updated_at",  # Дата последнего обновления записи о машине
        ]
        read_only_fields = ["owner"]  # Поле 'owner' доступно только для чтения, так как оно назначается автоматически при создании

class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    Преобразует объекты модели Comment в формат JSON и наоборот для использования в API.
    """

    class Meta:
        model = Comment  # Указываем модель, для которой создается сериализатор
        fields = [
            "id",          # Идентификатор комментария
            "content",     # Содержимое комментария
            "car",         # Машина, к которой относится комментарий (связь с моделью Car)
            "author",      # Автор комментария (связь с моделью User)
            "created_at",  # Дата создания комментария
        ]
        read_only_fields = ["author"]  # Поле 'author' доступно только для чтения, так как автор определяется автоматически
