import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freeporkbelly_main.settings")
django.setup()

from product.models import Category, Product, Option, OptionItems

CSV_PATH_OPTIONS = './project_options.csv'

with open(CSV_PATH_OPTIONS) as in_file:
    data_reader = csv.reader(in_file)
    for row in data_reader:
        option_type = row[0]
        # print(option_type)
        Option.objects.create(name = option_type)

        option_id = Option.objects.get(name = option_type).id
		
        option_items = row[1].split('.')
        print(option_items)
        
        for option_item in option_items:
            OptionItems.objects.create(name=option_item, option_id=option_id)
        
