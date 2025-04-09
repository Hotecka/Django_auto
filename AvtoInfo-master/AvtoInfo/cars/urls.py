from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cars import views
from cars import views_api


app_name = "cars"

router = DefaultRouter()
router.register(r"cars", views_api.CarViewSet)

urlpatterns = [
    path("", views.get_cars, name="home"),
    path("add/", views.add_car, name="add_car"),
    path("<int:car_id>/", views.car_detail, name="car_detail"),
    path("<int:car_id>/edit/", views.edit_car, name="edit_car"),
    path("<int:car_id>/delete/", views.delete_car, name="delete_car"),
    path("api/", include(router.urls)),
]
