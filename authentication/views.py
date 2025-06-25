from datetime import datetime, timedelta
import jwt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

SECRET_KEY = settings.SECRET_KEY

class RegisterView(APIView):
    def post(self, request):
        data = request.data 
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # input validation
        if not all([username, email, password]):
            return Response(
                {"error": "Username, email and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists, please use a different username"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already registered, please use a different email"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        token = jwt.encode(
            {"id": user.id, "exp": datetime.now() + timedelta(days=1)}, 
            SECRET_KEY, 
            algorithm="HS256"
        )

        return Response(
            {"message": "Registration successful", "token": token}, 
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):    
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        # input validation
        if not all([email, password]):
            return Response(
                {"error": "Email and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = authenticate(username=user.username, password=password)
        if user:
            token = jwt.encode(
                {"id": user.id, "exp": datetime.now() + timedelta(days=1)}, 
                SECRET_KEY, 
                algorithm="HS256"
            )
            return Response({"token": token}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"}, 
            status=status.HTTP_400_BAD_REQUEST
        )