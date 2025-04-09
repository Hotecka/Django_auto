from django.apps import AppConfig

class CarsConfig(AppConfig):
    """
    Конфигурация приложения для работы с автомобилями.
    Здесь можно задать настройки для приложения 'cars'.
    """

    default_auto_field = "django.db.models.BigAutoField"  # Устанавливаем тип для автоматического поля идентификатора (ID) - BigAutoField
    name = "cars"  # Имя приложения, используется для настройки в проекте Django

