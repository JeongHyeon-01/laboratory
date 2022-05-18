import jwt, bcrypt,datetime
from django.conf            import settings

from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response

from users.serializers import UserSerializers
from users.models      import Users


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
            "id"          : user.id,
            "exp"         : datetime.datetime.utcnow() + datetime.timedelta(days=12)
        }, settings.SECRET_KEY, settings.ALGORITHM, headers={"typ":"Bearer"})
        
        user.refresh_token = token 
        user.save()
        
        return Response({'refresh_token':token},status=status.HTTP_201_CREATED)

class UserSigninView(APIView):
    def post(self, request):
        if Users.objects.filter(name =request.data['name'],password = request.data['password']).exists():
            user = Users.objects.get(name =request.data['name'],password = request.data['password'])
            re_token = jwt.decode(user.refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
            token = jwt.encode({
                "id" : re_token['id'],
                "exp" : datetime.datetime.utcnow() + datetime.timedelta(days=6)
            })
            return Response({"access_token":token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


        