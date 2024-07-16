from rest_framework import serializers
from .models import Facility, Facility_Image, Facility_Booking, Amenity

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["uuid", "facility", "name"]
        extra_kwargs = {"uuid": {"read_only": True}}
    
class FacilityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility_Image
        fields = ["uuid", "facility", "image", "is_primary"]
        extra_kwargs = {"uuid": {"read_only": True}}

class FacilitySerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    images = FacilityImageSerializer(many=True, read_only=True)

    class Meta:
        model = Facility
        fields = ['uuid', 'owner', 'owner_username', 'name', 'category', 'description', 
                  'city', 'location_link', 'price_per_day', 'created_at', 'updated_at', 'amenities', 'images']
        extra_kwargs = {"created_at": {"read_only": True}, "updated_at": {"read_only": True}}

    def get_owner_username(self, obj):
        return obj.owner.username

    def get_amenities(self, obj):
        return [amenity.name for amenity in obj.amenities.all()]
    
class FacilityUpdateSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()
    class Meta:
        model = Facility
        fields = ['uuid', 'owner', 'owner_username', 'name', 'category', 'description', 
                  'city', 'location_link', 'price_per_day', 'created_at', 'updated_at']
        extra_kwargs = {"uuid": {"read_only": True}, "owner": {"read_only": True}, 
                        "created_at": {"read_only": True}, "updated_at": {"read_only": True}}

    def get_owner_username(self, obj):
        return obj.owner.username
    
class FacilityBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility_Booking
        fields = ["uuid", "facility", "booker", "start_date", "end_date", 
                  "duration", "notes", "is_approved", "is_paid"]
        extra_kwargs = {"uuid": {"read_only": True}, "duration": {"read_only": True},}

    def validate(self, data):
        instance = Facility_Booking(**data)
        instance.clean()
        return data
    
    def validate_start_date(self, value):
        if value is None:
            raise serializers.ValidationError("Start date must be provided.")
        return value

    def validate_duration(self, value):
        if value is None:
            raise serializers.ValidationError("Duration must be provided.")
        return value
    
class FacilityBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility_Booking
        fields = ["uuid", "facility", "booker", "start_date", "end_date", 
                  "duration", "notes", "is_approved", "is_paid"]
        extra_kwargs = {"uuid": {"read_only": True}, "facility": {"read_only": True}, 
                        "booker": {"read_only": True}, "start_date": {"read_only": True}, 
                        "end_date": {"read_only": True}, "duration": {"read_only": True}, }
