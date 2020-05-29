from django.urls import path

from .views import ProductView, CategoryView

urlpatterns = [
    path('/category/<int:category_id>', CategoryView.as_view(), name='category'),
    path('/detail/<int:product_id>', ProductView.as_view(), name='product'),
]