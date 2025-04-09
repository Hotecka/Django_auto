from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

from cars.serializers import CarSerializer, CommentSerializer
from cars.models import Car, Comment


class CarViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с API
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission = IsAuthenticated

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не владелец этой машины.")
        instance.delete()

    @action(detail=True, methods=["get", "post"])
    def comments(self, request, pk=None):
        car = self.get_object()

        if request.method == "GET":
            comments = Comment.objects.filter(car=car)
            serializer = CommentSerializer(comments, many=True)

            return Response(serializer.data)

        if request.method == "POST":
            content = request.data.get("content")
            comment = Comment.objects.create(
                content=content,
                car=car,
                author=request.user,
            )
            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=201)
