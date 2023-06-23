"""
Данный модуль импортирует csv-файл 'ingredients.csv' в базу данных.
Для запуска программы введите команду 'python manage.py import_data'.
"""

import csv
import os

from django.core.management import BaseCommand

from foodgram.settings import CSV_FILE_PATH
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Load from csv file into the database"

    def handle(self, *args, **kwargs):
        file = os.path.join(CSV_FILE_PATH, "ingredients.csv")
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=",")
                next(reader)

                Ingredient.objects.all().delete()

                for row in reader:
                    print(row)

                    record = Ingredient(name=row[0], measurement_unit=row[1])
                    record.save()

                cnt = Ingredient.objects.count()
                print("-" * 80)
                print(f"Loaded into model Ingredient: {cnt} row(s)")
