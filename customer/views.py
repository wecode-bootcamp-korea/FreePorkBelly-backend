import json
import bcrypt
import jwt

from django.views import View
from django.http  import HttpResponse, JsonResponse

from .models import Customer

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Customer.objects.filter(email=data['email']).exists():
                return HttpResponse(status=409)
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            Customer.objects.create(
                email=data['email'],
                password=hashed_password.decode('utf-8'),
            )
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = Customer.objects.get(email=data['email'])
        try:
            if Customer.objects.filter(email=data['email']).exists():
                    user = Customer.objects.get(email=data['email'])

                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({'email':data['email']},'SECRET',algorithm='HS256').decode('utf-8')
                        return JsonResponse({'token':token},status=200)
                    return HttpResponse(status=401)
            return HttpResponse(status=401)

        except KeyError:

            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
