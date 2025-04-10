from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,  # Форма для аутентификации пользователя
    UserCreationForm,    # Форма для создания нового пользователя
    UserChangeForm,      # Форма для изменения данных пользователя
)

from users.models import User  

# Форма для аутентификации пользователя
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User  # Модель пользователя, с которой связана форма
        fields = [
            "username",  # Поле для ввода логина
            "password",  # Поле для ввода пароля
        ]

# Форма для регистрации нового пользователя
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User  # Модель пользователя для регистрации
        fields = [
            "username",  # Поле для ввода логина
            "email",     # Поле для ввода email
            "password1", # Поле для ввода пароля
            "password2", # Поле для подтверждения пароля
        ]

    
    email = forms.CharField() 

# Форма для изменения профиля пользователя
class UserProfileForm(UserChangeForm):
    class Meta:
        model = User  # Модель пользователя для изменения профиля
        fields = [
            "username",  # Поле для ввода логина
            "email",     # Поле для ввода или изменения email
        ]

    
    email = forms.CharField() 
