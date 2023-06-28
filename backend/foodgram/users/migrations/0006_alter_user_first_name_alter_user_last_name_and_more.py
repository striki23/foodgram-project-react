# Generated by Django 4.2.1 on 2023-06-23 12:58

import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=50, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=50, verbose_name="Фамилия"),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=50, verbose_name="Пароль"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[users.validators.validate_username],
                verbose_name="Пользователь",
            ),
        ),
    ]
