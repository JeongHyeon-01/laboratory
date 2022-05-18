import jwt
from django.http import JsonResponse
from django.conf import settings

from users.models import Users


# def refresh_token_authorization(func):
#     def wrapper(self, request, *args, **kargs):
#         refresh_token = 