import json
from django.views     import View
from django.http      import HttpResponse, JsonResponse

from customer.models  import Customer
from product.models   import (
    Category, Product, ProductDescription, 
    Review, Option, OptionItems)
from order.models     import Cart, CartItem, Order, OrderStatus, PaymentMethod



class CartView(View):
    
    #@login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            cart = Cart.objects.filter(customer_id=request.customer.id).last()
            cart_items = CartItem.objects.filter(cart_id=cart.id, prodcut_id=data['product_id'])

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
                    selected_option_id = data['quantity'],
                    quantity = data['quantity']
                ).save()

                return HttpResponse(status=200)
        except KeyError:
            return HttpResponse(status=400)

    #@login_decorator
    def get(self, request):
        cart = Cart.objects.filter(customer_id=request.customer.id).last()
        cart_items = CartItem.objects.get(cart_id=cart.id).cartitem_set.all()

        data = [
            {
                'name' : Proudct.objects.get(id=cart.product_id).name,
                'sub_img_url' : Proudct.objects.get(id=cart.product_id).sub_img_url,
                'selected_option' : OptionItems.objects.get(id=cart_item.option_id).name,
                'sales_price' : Proudct.objects.get(id=cart.product_id).sales_price,
                'quantity' : cart_item.quantity
            } for cart_item in cart_items
        ]

        return JsonResponse({'data' : list(data), status =200)

    #@login_decorator
    def delete(self, request):
        data = json.loads(request.body)
        cart = Cart.objects.filter(customer_id=request.customer.id).last()

        CartItems.objects.filter(cart_id=cart.id, product_id=data['product_id']).delete()

        return HttpResponse(status=200)
        
        