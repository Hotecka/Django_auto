from django.contrib import admin

from cars.models import Car, Comment


# Регистрация модели Car в админ-панели
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


# Регистрация модели Comment в админ-панели
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
