import json
from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *

class CreateFacilityAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data

        new_facility = Facility.objects.create(
            owner=request.user,
            name=data.get("name"),
            category=data.get('category'),
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
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request, pk, format=None):
        try:
            facility = Facility.objects.get(pk=pk)
            serializer = FacilitySerializer(facility)
            return Response(serializer.data)
        except Facility.DoesNotExist:
            return Response({"message": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        try:
            facility = Facility.objects.get(pk=pk)
            serializer = FacilityUpdateSerializer(facility, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Facility.DoesNotExist:
            return Response({"message": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            facility = Facility.objects.get(pk=pk)
            facility.delete()
            return Response({"message": "Facility has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Facility.DoesNotExist:
            return Response({"message": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='exact')
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
    permission_classes = [IsAuthenticated]

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
    
class AmenityDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request, pk, format=None):
        try:
            amenity = Amenity.objects.get(pk=pk)
            serializer = AmenitySerializer(amenity)
            return Response(serializer.data)
        except Amenity.DoesNotExist:
            return Response({"message": "Amenity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        try:
            amenity = Amenity.objects.get(pk=pk)
            serializer = AmenitySerializer(amenity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Amenity.DoesNotExist:
            return Response({"message": "Amenity not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            amenity = Amenity.objects.get(pk=pk)
            amenity.delete()
            return Response({"message": "Amenity has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Amenity.DoesNotExist:
            return Response({"message": "Amenity not found"}, status=status.HTTP_404_NOT_FOUND)
        
class AddFacilityImageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            facility_id = request.data.get('facility', [])
            facility = Facility.objects.get(pk=facility_id)
        except Facility.DoesNotExist:
            return Response({"message": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FacilityImageSerializer(data=request.data, context={'facility': facility})
        if serializer.is_valid():
            serializer.save()
            replace_id = request.data.get('replace', [])
            replace = Facility_Image.objects.get(pk=replace_id)
            replace.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FacilityImageDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk, format=None):
        try:
            image = Facility_Image.objects.get(pk=pk)
            serializer = FacilityImageSerializer(image)
            return Response(serializer.data)
        except Facility_Image.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            image = Facility_Image.objects.get(pk=pk)
            image.delete()
            return Response({"message": "Image has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Facility_Image.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
    
class CreateFacilityBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FacilityBookingSerializer(data=request.data, context={'booker': request.user})
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
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk, format=None):
        try:
            booking = Facility_Booking.objects.get(pk=pk)
            serializer = FacilityBookingSerializer(booking)
            return Response(serializer.data)
        except Facility_Booking.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk, format=None):
        try:
            booking = Facility_Booking.objects.get(pk=pk)
            serializer = FacilityBookingUpdateSerializer(booking, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Facility_Booking.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            booking = Facility_Booking.objects.get(pk=pk)
            booking.delete()
            return Response({"message": "Booking has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Facility_Booking.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
class CreateFacilityReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FacilityReviewSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FacilityReviewDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request, pk, format=None):
        try:
            review = FacilityReview.objects.get(pk=pk)
            serializer = FacilityReviewSerializer(review)
            return Response(serializer.data)
        except FacilityReview.DoesNotExist:
            return Response({"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, format=None):
        try:
            review = FacilityReview.objects.get(pk=pk)
            serializer = FacilityReviewUpdateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FacilityReview.DoesNotExist:
            return Response({"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            review = FacilityReview.objects.get(pk=pk)
            review.delete()
            return Response({"message": "Review has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        except FacilityReview.DoesNotExist:
            return Response({"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        
class FacilityReviewFilter(filters.FilterSet):
    facility = filters.CharFilter(field_name='facility__uuid', lookup_expr='exact')
    user = filters.CharFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = FacilityReview
        fields = ['facility__uuid', 'user__id']

class FacilityReviewsListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = FacilityReview.objects.all()
    serializer_class = FacilityReviewSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FacilityReviewFilter