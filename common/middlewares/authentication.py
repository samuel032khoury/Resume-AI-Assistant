# 在 resume 目录下创建 middleware.py
import jwt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import login

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token and token.startswith('Bearer '):
            token = token[7:]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                
                user = User.objects.get(id=user_id)
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
                # If token is invalid or user does not exist, set user to AnonymousUser
                pass

        response = self.get_response(request)
        return response