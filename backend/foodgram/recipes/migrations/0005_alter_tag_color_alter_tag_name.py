# Generated by Django 4.2.1 on 2023-06-12 19:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0004_alter_tag_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                default="#FF0000", max_length=7, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
