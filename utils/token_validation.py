import jwt,datetime


from django.conf import settings
#유저가 리프레시 토큰을 가지고 있을때 exp 현재날짜와 비교해서 재발급
def check_refresh_exp(user):
    refresh_token = user.refresh_token
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
    now = datetime.datetime.now()
    print(datetime.datetime.timestamp(now))
    if payload['exp'] < datetime.datetime.timestamp(now):
        token = jwt.encode({
            "user_id"          : user.id,
            "exp"         : datetime.datetime.utcnow() + datetime.timedelta(days=12)
        }, settings.SECRET_KEY, settings.ALGORITHM, headers={"typ":"Bearer"})
        user.refresh_token = token
        user.save()
    else:
        pass

