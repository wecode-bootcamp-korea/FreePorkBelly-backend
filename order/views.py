import json
from django.views     import View
from django.http      import HttpResponse, JsonResponse

from customer.models  import Customer, DeliveryAddress
from product.models   import (
    Category, Product, ProductDescription, 
    Review, Option, OptionItems)
from order.models     import Cart, CartItem, Order, OrderStatus, PaymentMethod


class CartView(View):
    
    #@login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            if Cart.objects.filter(customer_id=data['customer_id']).exists():       # 해당 ID의 카트가 존재하면, 그거 가져옴
                cart = Cart.objects.filter(customer_id=data['customer_id']).last()
            else:
                cart = Cart.objects.create(customer_id=data['customer_id'])             # 없으면 카트를 신규로 생성

            cart_items = CartItem.objects.filter(cart_id=cart.id, product_id=data['product_id'])

            if cart_items.exists():
                cart_items.update(
                    selected_option_id = data['selected_option_id'],
                    quantity = data['quantity']
                )

                return HttpResponse(status=200)
            
            else:
                CartItem(
                    cart_id = cart.id,
                    product_id = data['product_id'],
                    selected_option_id = data['selected_option_id'],
                    quantity = data['quantity']
                ).save()

                return HttpResponse(status=200)
        except KeyError:
            return HttpResponse(status=400)

    #@login_decorator
    def get(self, request):
        cart = Cart.objects.filter(customer_id=request.GET.get('customer_id')).last()
        cart_items = CartItem.objects.filter(cart_id=cart.id)

        data = [
            {
                'name' : cart_item.product.name,
                'sub_img_url' : cart_item.product.sub_img_url,
                'selected_option' : OptionItems.objects.get(id=cart_item.selected_option_id).name,
                'sales_price' : cart_item.product.sales_price,
                'quantity' : cart_item.quantity
            } for cart_item in cart_items
        ]

        return JsonResponse({'data' : data}, status=200)

    #@login_decorator
    def delete(self, request):
        data = json.loads(request.body)
        
        cart = Cart.objects.filter(customer_id=data['customer_id']).last()
        CartItem.objects.filter(cart_id=cart.id, product_id=data['product_id']).delete()

        return HttpResponse(status=200)


class AddressView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)

            DeliveryAddress(
                customer_id = request.GET.get('customer_id'),   #parameter로 받을 것과 POST로 받을 것 정해야 함.
                name = data['name'],
                phone = data['phone'],
                address = data['address']
            ).save()

            return HttpResponse(status=200)
        
        except KeyError:
            return HttpResponse(status=400)
        
    def get(self, request):
        delivery_addresses = DeliveryAddress.objects.filter(customer_id=request.GET.get('customer_id'))

        data = [
            {
                'address_id' : delivery_address.id,
                'name' : delivery_address.name,
                'phone' : delivery_address.phone,
                'address' : delivery_address.address
            } for delivery_address in delivery_addresses
        ]

        return JsonResponse({'data' : data}, status=200)

    def delete(self, request):
        address_id = request.GET.get('address_id')

        DeliveryAddress.objects.get(id=address_id).delete()

        return HttpResponse(status=200)

