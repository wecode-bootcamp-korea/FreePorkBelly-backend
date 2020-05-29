from django.urls import path, include

urlpatterns = [
    path('customer', include('customer.urls')),
]
