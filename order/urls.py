from django.urls import path

from .views import CartView, AddressView, OrderView

urlpatterns = [
    path('/cart', CartView.as_view(), name='cart'),
    path('/address', AddressView.as_view(), name='address'),
    path('/payment', OrderView.as_view(), name='order')
]