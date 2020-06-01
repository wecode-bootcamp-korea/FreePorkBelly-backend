from django.urls import path, include

urlpatterns = [
    path('customer', include('customer.urls')),
    path('product', include('product.urls')),
    #path('order', include('order.urls')),
    #path('support', include('support.urls'))
]
