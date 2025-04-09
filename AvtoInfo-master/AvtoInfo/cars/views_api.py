from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

from cars.serializers import CarSerializer, CommentSerializer
from cars.models import Car, Comment


class CarViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с API по машинам.
    Обрабатывает стандартные CRUD операции для модели Car и дополнительные действия с комментариями.
    """

    queryset = Car.objects.all()  # Получаем все автомобили
    serializer_class = CarSerializer  # Сериализатор для модели Car
    permission_classes = [IsAuthenticated]  # Требуется аутентификация для всех действий

    def perform_create(self, serializer):
        """
        Переопределение метода create, чтобы при создании автомобиля 
        автоматически устанавливался владелец как текущий пользователь.
        """
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        """
        Переопределение метода delete, чтобы удалять автомобиль только если текущий пользователь является владельцем.
        В противном случае выбрасывается исключение PermissionDenied.
        """
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не владелец этой машины.")
        instance.delete()

    @action(detail=True, methods=["get", "post"])
    def comments(self, request, pk=None):
        """
        Дополнительный экшн для работы с комментариями машины.
        - GET: Получить все комментарии к автомобилю.
        - POST: Добавить новый комментарий к автомобилю.
        """
        car = self.get_object()  # Получаем объект автомобиля по ID (pk)

        if request.method == "GET":
            # Получаем все комментарии для данного автомобиля
            comments = Comment.objects.filter(car=car)
            serializer = CommentSerializer(comments, many=True)  # Сериализуем данные

            return Response(serializer.data)  # Возвращаем список комментариев

        if request.method == "POST":
            # Добавляем новый комментарий для данного автомобиля
            content = request.data.get("content")  # Получаем содержание комментария
            comment = Comment.objects.create(
                content=content,
                car=car,
                author=request.user,  # Автором комментария является текущий пользователь
            )
            serializer = CommentSerializer(comment)  # Сериализуем комментарий

            return Response(serializer.data, status=201)  # Возвращаем данные нового комментария с кодом 201
