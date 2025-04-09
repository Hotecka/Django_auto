from rest_framework import serializers
from cars.models import Car, Comment


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "id",
            "make",
            "model",
            "year",
            "description",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "car",
            "author",
            "created_at",
        ]
        read_only_fields = ["author"]
