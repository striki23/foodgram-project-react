"""
Данный модуль импортирует csv-файл 'ingredients.csv' в базу данных.
Для запуска программы введите команду 'python manage.py import_data'.
"""

import csv
import os

from django.core.management import BaseCommand
from optparse import make_option

from foodgram.settings import CSV_FILE_PATH
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Load from csv file into the database"


    def handle(self, *args, **options):
        file = os.path.join(CSV_FILE_PATH, "ingredients.csv")
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=",")
                next(reader)

                cnt = 0
                for row in reader:
                    print(row)
                    obj, created = Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1])
                    if created == True:
                        cnt += 1
                

                print("-" * 80)
                print(f"Loaded into model Ingredient: {cnt} row(s)")
