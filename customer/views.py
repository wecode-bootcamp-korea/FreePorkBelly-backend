import json
import bcrypt
import jwt

from django.views import View
from django.http  import HttpResponse, JsonResponse
#from django.db    import IntergrityError

from .models      import Customer

#import my_settings

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            Customer.objects.create(
                email=data['email'],
                password=hashed_password.decode('utf-8'),
                name=data['name'],
                phone=data['phone']
            )
            return HttpResponse(status=200)
        except TypeError:
            return JsonResponse({'message':'INVALID INPUT'}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
        # except IntegrityError:
        #     return JsonResponse({'message':'Already registered username'}, status=400)
        # except IntegrityError:
        #     return JsonResponse({'message':'Already registered email'}, status=400)
        

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Customer.objects.filter(email=data['email']).exists():
                customer = Customer.objects.get(email=data['email'])
                
                if bcrypt.checkpw(data['password'].encode('utf-8'), customer.password.encode('utf-8')):
                    token = jwt.encode({'customer_id':customer.id}, 'secret', algorithm='HS256').decode('utf-8')
                    return JsonResponse({'token' : token}, status=200)
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)
            else:
                return JsonResponse({"message" : "INVALID_USERNAME"}, status=400)
        
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


def login_decorator(func):
    
    def wrapper(self, request, *args, **kwargs):
        try:
            auth_token = request.headers.get('Authorization', None)
            #print('auth_token', auth_token)
            payload = jwt.decode(auth_token, 'secret', algorithm='HS256')
            #print('payload', payload)
            request.user = Customer.objects.get(id=payload['customer_id'])
            return func(self, request, *args, **kwargs)

        except Customer.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
    
    return wrapper