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
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter

class EditProfilePicAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        
        serializer = ProfilePicSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)