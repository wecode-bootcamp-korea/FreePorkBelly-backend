from django.urls import path

from .views import MainView, CategoryView, ProductView, ReviewView

urlpatterns = [
    path('/main', MainView.as_view(), name='main'),
    path('/', CategoryView.as_view(), name='category'),
    path('/<int:product_id>', ProductView.as_view(), name='product'),
    path('/review/<int:product_id>', ReviewView.as_view()),
]
