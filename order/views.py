import json
from django.views     import View
from django.http      import HttpResponse, JsonResponse
from decimal          import Decimal
import datetime

from customer.models  import Customer, DeliveryAddress
from customer.views   import login_decorator
from product.models   import (
    Category, Product, ProductDescription, 
    Review, Option, OptionItems)
from order.models     import Cart, CartItem, Order, OrderStatus, PaymentMethod


class CartView(View):    
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            customer_id = request.customer.id

            if Cart.objects.filter(customer_id=customer_id).exists():       # 해당 고객의 카트가 존재하면 가져옴
                cart = Cart.objects.get(customer_id=customer_id)
            else: # 해당 고객에게 카트가 없으면 카트를 신규로 생성하고, order_status_id를 부여
                cart = Cart.objects.create(customer_id=customer_id, cart_status_id=1)             

            cart_items = CartItem.objects.filter(cart_id=cart.id, product_id=data['product_id'])

            if cart_items.exists():
                cart_items.update(
                    quantity = data['quantity']
                )
                return HttpResponse(status=200)
            
            else:
                CartItem(
                    cart_id            = cart.id,
                    product_id         = data['product_id'],
                    selected_option_id = data['selected_option_id'],
                    quantity           = data['quantity']
                ).save()
                return HttpResponse(status=200)

        except KeyError:
            return HttpResponse(status=400)

    @login_decorator
    def get(self, request):
        try:
            customer_id = request.customer.id
            
            cart       = Cart.objects.get(customer_id=customer_id, cart_status_id=1)
            cart_items = CartItem.objects.select_related('product', 'selected_option').filter(cart_id=cart.id)

            total_amount = 0
            for cart_item in cart_items:
                total_amount += cart_item.product.sales_price * cart_item.quantity
            
            delivery_cost = 0
            expected_amount = total_amount + delivery_cost

            cart_items = [
                {
                    'cart_item_id'    : cart_item.id,
                    'product_id'      : cart_item.product.id,
                    'name'            : cart_item.product.name,
                    'sub_img_url'     : cart_item.product.sub_img_url,
                    'selected_option' : OptionItems.objects.get(id=cart_item.selected_option_id).name,
                    'sales_price'     : cart_item.product.sales_price,
                    'per_quantity'    : cart_item.product.sales_price_comment.split('(')[1].replace(')', ' 기준'),
                    # sales_price_comment 기준가 xx원 (600g) 에서 600g 파싱한 뒤,' 기준' 멘트 추가 
                    'quantity'        : cart_item.quantity
                } for cart_item in cart_items
            ]

            cart = [
                {
                    'cart_id'         : cart.id,
                    'total_amount'    : total_amount,
                    'delivery_cost'   : delivery_cost,
                    'expected_amount' : expected_amount
                }
            ]

            return JsonResponse({'cart_items' : cart_items, 'cart' : cart}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_EXIST'}, status=200)

    @login_decorator
    def delete(self, request):
        data        = json.loads(request.body)
        customer_id = request.customer.id

        cart = Cart.objects.get(customer_id=customer_id)
        CartItem.objects.get(cart_id=cart.id, product_id=data['product_id']).delete()

        return HttpResponse(status=200)
    

class AddressView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            customer_id = request.customer.id

            # DeliverAddress 복수 등록 가능하게 Model 설계되었으나, 프론트와 연동 편의성 위해 1개만 등록. 이후에 업데이트되도록 로직 수정
            if DeliveryAddress.objects.filter(customer_id=customer_id).exists():
                DeliveryAddress.objects.filter(customer_id=customer_id).update(
                    name    = data['name'],
                    phone   = data['phone'],
                    address = data['address']
                )
                return HttpResponse(status=200)
            
            else: 
                DeliveryAddress(
                    customer_id = customer_id,   
                    name        = data['name'],
                    phone       = data['phone'],
                    address     = data['address']
                ).save()

                return HttpResponse(status=200)
        
        except KeyError:
            return HttpResponse(status=400)

    @login_decorator    
    def get(self, request):
        customer_id        = request.customer.id
        delivery_addresses = DeliveryAddress.objects.filter(customer_id=customer_id)
        
        data = [
            {
                'address_id' : delivery_address.id,
                'name'       : delivery_address.name,
                'phone'      : delivery_address.phone,
                'address'    : delivery_address.address
            } for delivery_address in delivery_addresses
        ]

        return JsonResponse({'data' : data}, status=200)

    @login_decorator  
    def delete(self, request):
        address_id = request.GET.get('address_id')
        DeliveryAddress.objects.get(id=address_id).delete()

        return HttpResponse(status=200)


class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            customer_id = request.customer.id

            cart             = Cart.objects.get(customer_id=customer_id)
            delivery_address = DeliveryAddress.objects.get(customer_id=customer_id)
            expected_amount  = Decimal(data['expected_amount'])

            # Order 객체 생성
            Order(
                customer_id         = customer_id,
                cart_id             = cart.id,
                payment_amount      = expected_amount,        
                payment_method_id   = 2,                           # 프론트엔드에서 무통장입금만 구현하여 무통장인 2번으로 부여
                order_status_id     = 4,                             # 오더완료 시, status를 결제완료로 세팅
                delivery_address_id = delivery_address.id
            ).save()

            # Cart Status를 주문완료로 변경한 후 Cart 객체 삭제 -> 장바구니에 가면 비어있게 됨
            cart.cart_status_id = 3
            cart.save()

            return HttpResponse(status=200)
        
        except KeyError:
            return HttpResponse(status=400)
    
    @login_decorator
    def get(self, request):
        customer_id = request.customer.id
        try:
            orders = Order.objects.select_related('cart').prefetch_related('cart__cartitem_set').filter(customer_id=customer_id).order_by('-order_date')

            data = [
                {
                    'order_id'      : order.id,
                    'order_date'    : order.order_date,
                    'order_item'    : [{
                        'item_name' : order_item.product.name,
                        'quantity'  : order_item.quantity
                    } for order_item in order.cart.cartitem_set.all()],
                    'total_amount'  : order.payment_amount,
                    'arrival_time'  : order.order_date + datetime.timedelta(days=1)     # 오더 확정 후 1일 후 배송되는 것으로 설정
                } for order in orders]

            return JsonResponse({'data' : data}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'message' : 'ORDER_NOT_EXIST'}, status=200)