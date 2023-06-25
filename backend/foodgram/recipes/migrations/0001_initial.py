# Generated by Django 4.2.1 on 2023-05-19 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AmountIngredient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Количество"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Количество ингредиентов",
                "ordering": ("recipe",),
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Название ингридиента"
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(
                        max_length=10, verbose_name="Единица измерения"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингридиент",
                "verbose_name_plural": "Ингридиенты",
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название рецепта",
                        max_length=100,
                        verbose_name="Название рецепта",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Введите текст поста",
                        verbose_name="Описание приготовления",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="recipes/images/",
                        verbose_name="Фото блюда",
                    ),
                ),
                (
                    "cooking_time",
                    models.PositiveIntegerField(
                        verbose_name="Время приготовления в минутах"
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ["-pub_date"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("color", models.CharField(default="#ffffff", max_length=7)),
                ("slug", models.SlugField(unique=True, verbose_name="тег")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
    ]
