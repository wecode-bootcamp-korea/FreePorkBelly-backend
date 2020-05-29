import json
from django.views     import View
from django.http      import HttpResponse, JsonResponse

from customer.models  import Customer
from product.models   import (
    Category, Product, ProductDescription, 
    Review, Option, OptionItems)

from django.shortcuts import render

class CategoryView(View):
    def get(self, request, category_id):

        try:
            
            if category_id == 0:                  # 0일 때는 실행되나, category_id가 빈 값일 때는 에러 발생
                category_info = {
                    'name' : "전체보기",
                    'image_url' : "https://www.jeongyookgak.com/assets/list/01.png"
                }

                products = Product.objects.all()
            else:
                category = Category.objects.get(id=category_id)
                products = Product.objects.filter(category_id=category_id)

                category_info = {
                    'name' : category.name,
                    'image_url' : category.image_url
                }
            # product_info는 좀 수정이 필요해 보임.
            products_info = [{
                    'product_id' : category_id,
                    'name' : product.name,
                    'unit_price_comment' : product.unit_price_comment,
                    'sales_price_comment' : product.sales_price_comment,
                    'sub_img_url' : product.sub_img_url
                } for product in products]

            return JsonResponse({'category_info' : category_info, 'products_info' : products_info}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({'message' : "INVALID_CATEGORY_ID"})


class ProductView(View):
    def get(self, request, product_id):
        
        try:
            product = Product.objects.get(id = product_id)

            # 옵션사항 리스트로 가져오기
            option_id = product.option.id
            options = product.option.optionitems_set.filter(option_id = option_id)
            option_list = [option.name for option in options]
            
            # ProductDetail 설명 파트에서 사용될 이미지 리스트 가져오기
            desc_imgs = product.productdescription_set.all()
            desc_img_list = [ desc_img.img_url for desc_img in desc_imgs ]            

            product_detail = {
                'name' : product.name,
                'unit_price_comment' : product.unit_price_comment,
                'unit_price' : product.unit_price,
                'sales_price_comment' : product.sales_price_comment,
                'sales_price' : product.sales_price,
                'sub_img_url' : product.sub_img_url,
                'main_img_url' : product.main_img_url,
                'option_img_url' : product.option_img_url,
                'option_list' : option_list,
                'desc_img_list' : desc_img_list,
                'fresh_comment' : product.category.fresh_comment,
                'produced_date' : product.category.produced_date,
            }

            return JsonResponse({'product_detail' : product_detail}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : "INVALID_PRODUCT_ID"})