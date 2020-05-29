import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freeporkbelly_main.settings")
django.setup()

from product.models import Category

CSV_PATH_PRODUCTS = './project_categories.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    for row in data_reader:
        category_name = row[0]
        image_url = row[1]
        fresh_comment = row[2]
        produced_date = row[3]

        Category.objects.create(name = category_name, image_url = image_url, fresh_comment = fresh_comment, produced_date = produced_date)
