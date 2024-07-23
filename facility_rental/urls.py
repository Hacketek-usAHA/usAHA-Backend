from django.urls import path
from .views import *

urlpatterns = [
    path('', FacilitiesListAPIView.as_view(), name='all-facilities'),
    path('owner/', OwnerFacilitiesAPIView.as_view(), name='owner-facilities'),
    path('facility/create/', CreateFacilityAPIView.as_view(), name='create-facility'),
    path('facility/<uuid:pk>/', FacilityDetailAPIView.as_view(), name='facility'),
    path('amenity/create/', AddAmenityAPIView.as_view(), name='create-amenity'),
    path('amenity/<uuid:pk>/', AmenityDetailAPIView.as_view(), name='amenity'),
    path('image/create/', AddFacilityImageAPIView.as_view(), name='create-image'),
    path('image/<uuid:pk>/', FacilityImageDetailAPIView.as_view(), name='image'),
    path('bookings/', FacilityBookingsListAPIView.as_view(), name='bookings'),
    path('bookings/user/', UserFacilityBookingsAPIView.as_view(), name='user-bookings'),
    path('booking/create/', CreateFacilityBookingAPIView.as_view(), name='create-booking'),
    path('booking/<uuid:pk>/', BookingDetailAPIView.as_view(), name='booking'),
    path('reviews/', FacilityReviewsListAPIView.as_view(), name='reviews'),
    path('review/create/', CreateFacilityReviewAPIView.as_view(), name='create-review'),
    path('review/<uuid:pk>/', FacilityReviewDetailAPIView.as_view(), name='review'),
]