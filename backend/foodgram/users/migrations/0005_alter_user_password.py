# Generated by Django 4.2.1 on 2023-06-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_remove_subscribe_unique_follow_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=150, verbose_name="Пароль"),
        ),
    ]
