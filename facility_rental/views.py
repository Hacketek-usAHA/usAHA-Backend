import json
from rest_framework import generics, status
from django.views.decorators.csrf import csrf_exempt
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
        user = CustomUser.objects.get(id=data.get('owner'))

        new_facility = Facility.objects.create(
            owner=user,
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
    
class FacilitiesListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, query=None, format=None):
        if query is None or query.strip() == "":
            facilities = Facility.objects.all()
        else:
            facilities = Facility.objects.filter(name__icontains=query)
        
        serializer = FacilitySerializer(facilities, many=True)
        return Response(serializer.data)

class CreateAmenityAPIView(APIView):
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