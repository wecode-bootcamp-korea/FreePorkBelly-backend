from django.db import models

from customer.models import Customer


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_url = models.URLField(max_length=2000)
    fresh_comment = models.CharField(max_length=300, null=True)
    produced_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
    

class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, unique=True)
    unit_price_comment = models.CharField(max_length=300)                 # 상품별로 단위가 달라서 단위가격 코멘트가 다 상이함
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price_comment = models.CharField(max_length=300)                # 상품별로 판매단위가 다 달라 판매가격 코멘트가 다 상이함
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    main_img_url = models.URLField(max_length=2000)   # 상품 디테일 화면에 뿌려지는 black 배경 이미지 
    sub_img_url = models.URLField(max_length=2000)    # 카테고리에서 뿌려지는 white 배경 이미지
    option_img_url = models.URLField(max_length=2000, null=True)
    option = models.ForeignKey('Option', on_delete=models.SET_NULL, null=True) # option과 1대1 관계
    information = models.CharField(max_length=2000)  # 상품 기본정보 -> 실제 반영할지는 추후 판단함

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'

class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    img_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'product_descriptions'

class Review(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'reviews'

class Option(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'options'

class OptionItems(models.Model):
    option = models.ForeignKey('Option', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'option_items'







