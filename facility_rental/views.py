import json
from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Facility, Amenity, Facility_Booking, Facility_Image
from authentication.models import CustomUser
from .serializers import FacilitySerializer, AmenitySerializer, FacilityBookingSerializer, FacilityImageSerializer

class CreateFacilityAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        owner = CustomUser.objects.get(id=data.get('owner'))

        new_facility = Facility.objects.create(
            owner=owner,
            name=data.get("name"),
            description=data.get("description"),
            city=data.get("city"),
            location_link=data.get("location_link"),
            price_per_day=data.get("price_per_day"),
        )

        images = request.FILES.getlist('images')
        for index, image in enumerate(images):
            Facility_Image.objects.create(
                facility=new_facility,
                image=image,
                is_primary=(index == 0)
            )

        amenities = request.data.get('amenities', [])
        if isinstance(amenities, str):
            try:
                amenities = json.loads(amenities)
            except json.JSONDecodeError:
                amenities = [amenities]

        for amenity in amenities:
            Amenity.objects.create(
                facility=new_facility,
                name=amenity.get('name')
            )
        serializer = self.get_serializer(new_facility)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FacilityDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        try:
            facility = Facility.objects.get(pk=pk)
            serializer = FacilitySerializer(facility)
            return Response(serializer.data)
        except Facility.DoesNotExist:
            return Response({"message": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        facility = Facility.objects.get(pk=pk)
        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        facility = Facility.objects.get(pk=pk)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    owner = filters.CharFilter(field_name='owner__id', lookup_expr='exact')

    class Meta:
        model = Facility
        fields = ['name', 'category', 'owner']

class FacilitiesListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FacilityFilter

class AddAmenityAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            facility_id = request.data.get('facility', [])
            facility = Facility.objects.get(pk=facility_id)
        except Facility.DoesNotExist:
            return Response({"message": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AmenitySerializer(data=request.data, context={'facility': facility})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateFacilityBookingAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = FacilityBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FacilityBookingFilter(filters.FilterSet):
    facility = filters.CharFilter(field_name='facility__uuid', lookup_expr='exact')
    booker = filters.CharFilter(field_name='booker__id', lookup_expr='exact')

    class Meta:
        model = Facility_Booking
        fields = ['facility__uuid', 'booker__id']

class FacilityBookingsListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Facility_Booking.objects.all()
    serializer_class = FacilityBookingSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FacilityBookingFilter

class BookingDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        try:
            booking = Facility_Booking.objects.get(pk=pk)
            serializer = FacilityBookingSerializer(booking)
            return Response(serializer.data)
        except Facility_Booking.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk, format=None):
        booking = self.get_object(pk)
        serializer = FacilityBookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        booking = Facility_Booking.objects.get(pk=pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)