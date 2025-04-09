from django.contrib import admin

from cars.models import Car, Comment


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
