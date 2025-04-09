from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        db_table: str = "Users"
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"

    def __str__(self) -> str:
        return self.username
