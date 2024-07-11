from django.urls import path
from .views import *

urlpatterns = [
    path('all-profiles/', ProfileListAPIView.as_view(), name='profiles'),
]