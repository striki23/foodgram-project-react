# Generated by Django 4.2.1 on 2023-06-15 20:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0007_favorite_favorite_uniq_favorite_user_recipe"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Favorite",
            new_name="FavoriteRecipe",
        ),
    ]
