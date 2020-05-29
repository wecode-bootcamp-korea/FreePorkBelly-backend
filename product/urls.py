from django.urls import path

from .views import ProductView

urlpatterns = [
    path('/detail/<int:product_id>', ProductView.as_view(), name='product'),
]