import jwt, bcrypt,datetime
from django.conf            import settings

from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response

from django.http       import HttpResponse, JsonResponse
from users.serializers import UserSerializers
from users.models      import Users
from utils .token_validation   import check_refresh_exp

class UserSignupView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] :
            password = data['password']
            password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

        info = {
            "name" : data['name'],
            "password" : password,
        } 

        serializer = UserSerializers(data = info)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = jwt.encode({
            "user_id"          : user.id,
            "exp"         : datetime.datetime.utcnow() + datetime.timedelta(days=12)
        }, settings.SECRET_KEY, settings.ALGORITHM, headers={"typ":"Bearer"}).decode('utf-8')
        
        user.refresh_token = token 
        user.save()
        
        return Response({'refresh_token':token},status=status.HTTP_201_CREATED)

class UserSigninView(APIView):
    def post(self, request):
        users = Users.objects.filter(name =request.data['name'])
        if users.exists():
            user= Users.objects.get(name=request.data['name'])
            check_refresh_exp(user=user)
        
        if bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password.encode('utf-8')):
            access_token = jwt.encode({'user_id':user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return Response({'access_token':access_token}, status=status.HTTP_200_OK)
        
        return Response({"message" : "YOUR ID or Password is Wrong"}, status = 400)


        



        