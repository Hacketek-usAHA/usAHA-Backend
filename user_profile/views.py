from django_filters import rest_framework as filters
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile
from .serializers import ProfileSerializer

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
