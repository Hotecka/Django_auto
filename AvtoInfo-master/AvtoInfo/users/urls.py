from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),  # Страница входа
    path("registration/", views.registration, name="registration"),  # Страница регистрации
    path("profile/", views.profile, name="profile"),  # Страница профиля пользователя
    path("logout/", views.logout, name="logout"),  # Страница выхода
]
