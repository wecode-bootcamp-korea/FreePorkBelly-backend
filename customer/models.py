from django.db import models

class Customer(models.Model):
    email    = models.CharField(max_length=50)
    password = models.CharField(max_length=300) 
    name     = models.CharField(max_length=300)
    phone    = models.CharField(max_length=50)
    coupons   = models.ManyToManyField('Coupon', related_name='coupons', through='CouponCustomer')
    bank     = models.ForeignKey('Bank',on_delete=models.SET_NULL,null=True)    

    class Meta:
        db_table = 'customers'

class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    name     = models.CharField(max_length=100)
    phone    = models.CharField(max_length=50)
    address  = models.CharField(max_length=300)
 
    class Meta:
        db_table = 'delivery_address'

class Coupon(models.Model):
    created_at   = models.DateTimeField(auto_now_add=True)
    name         = models.CharField(max_length=200)
    condition    = models.CharField(max_length=500)
    issued_at    = models.DateTimeField() 
    expired_date = models.DateTimeField()
    discount     = models.DecimalField(max_digits=10, decimal_places=2)
    status       = models.CharField(max_length=50)

    class Meta:
        db_table = 'coupons'

class CouponCustomer(models.Model):
    coupon   = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'coupon_customers'

class Point(models.Model):
    customer   = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField()
    comment    = models.CharField(max_length=45)
    amount     = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'points'

class Credit(models.Model):
    customer        = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    name            = models.CharField(max_length=50)
    birthday        = models.CharField(max_length=6)
    business_number = models.CharField(max_length=10)
    card_number     = models.CharField(max_length=18)
    valid_month     = models.CharField(max_length=2)
    valid_year      = models.CharField(max_length=2)
    password        = models.CharField(max_length=2)    

    class Meta:
        db_table = 'credits'

class Bank(models.Model):
    bank_name = models.CharField(max_length=50)
    account   = models.CharField(max_length=50)
    name      = models.CharField(max_length=50)
    phone     = models.CharField(max_length=50)
    email     = models.CharField(max_length=50)
 
    class Meta:
        db_table = 'banks'