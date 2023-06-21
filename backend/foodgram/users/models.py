from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Пользователь",
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name="E-Mail",
        unique=True,
        max_length=254,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=150, blank=False, null=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=False, null=False
    )
    password = models.CharField(
        verbose_name="Пароль", max_length=150, blank=False, null=False
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="Данная подписка уже существует",
            ),
            models.CheckConstraint(
                name="Нельзя подписаться на самого себя",
                check=~models.Q(author=models.F("user")),
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
