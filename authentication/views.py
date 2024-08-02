from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db import transaction
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .serializers import CustomUserSerializer
from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer
import jwt, datetime

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
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials!')

        login(request, user)

        response = Response()

        response.delete_cookie(
            'jwt',
            path='/',
            samesite='None',
            secure=False
        )

        payload = {
            'id': str(user.id),
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response.set_cookie(key='jwt', value=token, httponly=True, expires=payload['exp'], samesite='None', secure=True)

        response.data = {
            'jwt': token
        }
        
        return response
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie(
            'jwt',
            path='/',
            samesite='None',
            secure=False
        )
        response.data = {
            'message': 'Logout successful'
        }
        print(self.request.user)
        return response
    
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = Profile.objects.filter(user=user).first()

        user_serializer = CustomUserSerializer(user)
        profile_serializer = ProfileSerializer(profile)

        user_profile = {**user_serializer.data, **profile_serializer.data}
        return Response(user_profile)
    
    def put(self, request):
        user = request.user
        profile = Profile.objects.filter(user=user).first()

        user_data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
        }

        profile_data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "bio": request.data.get("bio"),
            "contact_number": request.data.get("contact_number"),
            "profile_pic": request.data.get("profile_pic"),
        }

        user_serializer = CustomUserSerializer(user, data=user_data, partial=True)
        profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()

            user_profile = {**user_serializer.data, **profile_serializer.data}
            return Response(user_profile)

        errors = {**user_serializer.errors, **profile_serializer.errors}
        return Response(errors, status=400)

    def patch(self, request):
        return self.put(request)
        
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]






