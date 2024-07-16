from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile
from .serializers import ProfileSerializer, ProfilePicSerializer
import jwt

User = get_user_model()

class ProfileFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Profile
        fields = ['user']

class ProfileListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter

class EditProfilePicAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, format=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        profile = Profile.objects.filter(user=user).first()

        if user is None or profile is None:
            raise AuthenticationFailed('User or profile not found!')
        
        serializer = ProfilePicSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)