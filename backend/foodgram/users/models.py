from django.contrib.auth.models import AbstractUser
from django.db import models

from api.myconstants import *
from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=LENGTH_SHORTWORD,
        verbose_name="Пользователь",
        validators=(validate_username,),
        unique=True,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        max_length=LENGTH_EMAIL,
        verbose_name="E-Mail",
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=LENGTH_SHORTWORD,
        verbose_name="Имя",
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        max_length=LENGTH_SHORTWORD,
        verbose_name="Фамилия",
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=LENGTH_SHORTWORD,
        verbose_name="Пароль",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


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
