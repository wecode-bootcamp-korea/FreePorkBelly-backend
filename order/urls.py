from django.urls import path

from .views import CartView, AddressView

urlpatterns = [
    path('/cart', CartView.as_view(), name='cart'),
    path('/address', AddressView.as_view(), name='address')
]