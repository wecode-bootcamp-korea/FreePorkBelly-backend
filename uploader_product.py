import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freeporkbelly_main.settings")  # 프로젝트명.settings
django.setup()

from product.models import Category, Product, ProductDescription, Option, OptionItems

CSV_PATH_PRODUCTS = './project_products.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        #print("row =",end=""),print(row)
        name = row[1]
        category_id = row[2]
        unit_price_comment = row[3]
        unit_price = float(row[4])
        sales_price_comment = row[5]
        sales_price = float(row[6])
        sub_img_url = row[7]
        main_img_url = row[8]
        option_img_url = row[9]
        option_id = row[13]
        # print(name, unit_price_comment, unit_price, type(unit_price))

        Product.objects.create(
			name = name, 
			category_id = category_id,
            unit_price_comment = unit_price_comment,
			unit_price = unit_price,
			sales_price_comment = sales_price_comment,
			sales_price = sales_price,
			main_img_url = main_img_url,
			sub_img_url = sub_img_url,
			option_img_url = option_img_url,
			option_id = option_id)
        p_id = Product.objects.get(name = name).id
		
        first_image = row[10]
        second_image = row[11]
        third_image = row[12]
        # print(first_image) 
        # print(second_image)
        # print(third_image)

        ProductDescription.objects.create(img_url = first_image, product_id = p_id, photo_order=1)
        ProductDescription.objects.create(img_url = second_image, product_id = p_id, photo_order=2)
        ProductDescription.objects.create(img_url = third_image, product_id = p_id, photo_order=3)
