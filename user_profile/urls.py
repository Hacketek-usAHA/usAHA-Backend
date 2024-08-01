from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileListAPIView.as_view(), name='profiles'),
    path('pfp/edit/', EditProfilePicAPIView.as_view(), name='edit-pfp'),
]