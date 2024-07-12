from django.urls import path
from .views import *

urlpatterns = [
    path('', FacilitiesListAPIView.as_view(), name='all-facilities'),
    path('facility/create/', CreateFacilityAPIView.as_view(), name='create-facility'),
    path('facility/<uuid:pk>/', FacilityDetailAPIView.as_view(), name='facility'),
    path('amenity/create/', AddAmenityAPIView.as_view(), name='create-amenity'),
    path('booking/', FacilityBookingsListAPIView.as_view(), name='bookings'),
    path('booking/create/', CreateFacilityBookingAPIView.as_view(), name='create-booking'),
    path('booking/<uuid:pk>/', BookingDetailAPIView.as_view(), name='booking'),
]