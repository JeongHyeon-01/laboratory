import jwt                                                

from django.http import JsonResponse 
from my_settings  import SECRET_KEY
from users.models import Users

def login_decorator(func):
    def wrapper(self, request,*args, **kwargs):
        auth_token = request.headers.get("Authorization", None)
        if auth_token == None:
            return JsonResponse({'message':'Enter the token'}, status=401)

        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms='HS256')
            if Users.objects.get(id=payload['user_id']):
                user = Users.objects.get(id=payload['user_id'])
                request.user = user
                return func(self, request,*args, **kwargs)
        except jwt.InvalidSignatureError:
            return JsonResponse({'message':'Invalid token. Check the suffix.'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'message':'Invalid token. Check the prefix.'}, status=401)

    return wrapper
