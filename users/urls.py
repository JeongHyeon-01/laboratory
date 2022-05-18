from django.urls import path,include
from users.views import UserSignupView,UserSigninView

urlpatterns = [
    path('signup', UserSignupView.as_view()),
    path('signin', UserSigninView.as_view())
]
