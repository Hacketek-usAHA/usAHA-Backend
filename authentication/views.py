from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomUserSerializer
from .models import CustomUser
from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer

User = get_user_model()

class CreateUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_serializer = CustomUserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not profile_serializer.is_valid():
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user = user_serializer.save()
            profile_serializer = ProfileSerializer(data=request.data, context={'user': user})
            if profile_serializer.is_valid():
                profile_serializer.save()

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        
{
    "username": "Najmi",
    "email": "najmibriliant@gmail.com",
    "password": "password",
    "first_name": "Najmi",
    "last_name": "Briliant",
    "bio": "FASILKOM 22",
    "contact_number": "123456789"
}
        
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
