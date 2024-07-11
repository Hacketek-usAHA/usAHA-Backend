from django.urls import path
from .views import *

urlpatterns = [
    path('', FacilitiesListAPIView.as_view(), name='all-facilities'),
    path('<str:query>/', FacilitiesListAPIView.as_view(), name='facilities'),
    path('facility/create/', CreateFacilityAPIView.as_view(), name='create-facility'),
    path('facility/<uuid:pk>/', FacilityDetailAPIView.as_view(), name='facility'),
    path('amenity/create/', CreateAmenityAPIView.as_view(), name='create-amenity'),
]