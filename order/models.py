from django.db import models

from customer.models import Customer, Coupon
from product.models  import Product, OptionItems

class Order(models.Model):
    customer         = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True)
    cart             = models.ForeignKey('Cart', on_delete=models.SET_NULL, null=True)
    coupon           = models.ForeignKey('customer.Coupon', on_delete=models.SET_NULL, null=True)
    point_amount     = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_amount   = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method   = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
    order_status     = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey('customer.DeliveryAddress', on_delete=models.SET_NULL, null=True)
    order_date       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_statuses'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'payment_methods'

class Cart(models.Model):
    customer   = models.ForeignKey('customer.Customer',on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'

class CartItem(models.Model):
    cart            = models.ForeignKey('Cart',on_delete=models.SET_NULL,null=True)
    product         = models.ForeignKey('product.Product',on_delete=models.SET_NULL,null=True)
    selected_option = models.ForeignKey('product.OptionItems',on_delete=models.SET_NULL,null=True)
    quantity        = models.IntegerField()

    class Meta:
        db_table = 'cart_items'