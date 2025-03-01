from rest_framework import serializers
from .models import *
from user_profile.models import Profile

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

class CreateFacilitySerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner_pfp = serializers.SerializerMethodField()
    owner_start = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    images = FacilityImageSerializer(many=True, read_only=True)

    class Meta:
        model = Facility
        fields = ['uuid', 'owner', 'owner_name', 'owner_pfp', 
                  'owner_start', 'name', 'category', 'description', 
                  'city', 'location_link', 'price_per_day', 'rating',
                  'created_at', 'updated_at', 'amenities', 'images']
        extra_kwargs = {"owner": {"read_only": True}, "rating": {"read_only": True},
                        "created_at": {"read_only": True}, "updated_at": {"read_only": True}}

    def get_owner_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.owner)
            owner_name = f"{profile.first_name} {profile.last_name}"
            return owner_name if owner_name else None
        except Profile.DoesNotExist:
            return None
        
    def get_owner_start(self, obj):
        return obj.owner.date_joined
    
    def get_owner_pfp(self, obj):
        try:
            profile = Profile.objects.get(user=obj.owner)
            return profile.profile_pic.url if profile.profile_pic else None
        except Profile.DoesNotExist:
            return None

    def get_amenities(self, obj):
        return [amenity.name for amenity in obj.amenities.all()]

class FacilitySerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner_pfp = serializers.SerializerMethodField()
    owner_start = serializers.SerializerMethodField()
    amenities = AmenitySerializer(many=True, read_only=True)
    images = FacilityImageSerializer(many=True, read_only=True)

    class Meta:
        model = Facility
        fields = ['uuid', 'owner', 'owner_name', 'owner_pfp', 
                  'owner_start', 'name', 'category', 'description', 
                  'city', 'location_link', 'price_per_day', 'rating',
                  'created_at', 'updated_at', 'amenities', 'images']
        extra_kwargs = {"owner": {"read_only": True}, "rating": {"read_only": True},
                        "created_at": {"read_only": True}, "updated_at": {"read_only": True}}

    def get_owner_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.owner)
            owner_name = f"{profile.first_name} {profile.last_name}"
            return owner_name if owner_name else None
        except Profile.DoesNotExist:
            return None
        
    def get_owner_start(self, obj):
        return obj.owner.date_joined
    
    def get_owner_pfp(self, obj):
        try:
            profile = Profile.objects.get(user=obj.owner)
            return profile.profile_pic.url if profile.profile_pic else None
        except Profile.DoesNotExist:
            return None

    
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
    user_rating = serializers.SerializerMethodField()
    facility_name = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    price_per_day = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Facility_Booking
        fields = ["uuid", "facility", "booker", "start_date", "end_date", 
                  "duration", "notes", "is_approved", "is_paid", "user_rating", 
                  "facility_name", "city", "price_per_day", "image"]
        extra_kwargs = {"uuid": {"read_only": True}, "booker": {"read_only": True}, 
                        "is_paid": {"read_only": True}, "is_approved": {"read_only": True},
                        "duration": {"read_only": True}, "user_rating": {"read_only": True},
                        "facility_name": {"read_only": True}, "city": {"read_only": True},
                        "price_per_day": {"read_only": True}, "image": {"read_only": True},}
        
    def get_user_rating(self, obj):
        try:
            return obj.review.rating
        except FacilityReview.DoesNotExist:
            return None
    
    def get_facility_name(self, obj):
        return obj.facility.name

    def get_city(self, obj):
        return obj.facility.city
    
    def get_price_per_day(self, obj):
        return obj.facility.price_per_day
    
    def get_image(self, obj):
        primary_image = obj.facility.images.filter(is_primary=True).first()
        return FacilityImageSerializer(primary_image).data if primary_image else None

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
    
    def create(self, validated_data):
        booker = self.context.get('booker')
        booking = Facility_Booking.objects.create(booker=booker, **validated_data)
        return booking
    
class FacilityBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility_Booking
        fields = ["uuid", "facility", "booker", "start_date", "end_date", 
                  "duration", "notes", "is_approved", "is_paid"]
        extra_kwargs = {"uuid": {"read_only": True}, "facility": {"read_only": True}, 
                        "booker": {"read_only": True}, "start_date": {"read_only": True}, 
                        "end_date": {"read_only": True}, "duration": {"read_only": True}, 
                        "is_paid": {"read_only": True}}
        
class FacilityReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_pfp = serializers.SerializerMethodField()
    user_start = serializers.SerializerMethodField()
    facility_name = serializers.SerializerMethodField()

    class Meta:
        model = FacilityReview
        fields = ["id", "user", "user_name", "user_pfp", "user_start", 
                  "booking", "facility", "facility_name", "rating", 
                  "content", "created_at", "updated_at"]
        extra_kwargs = {"id": {"read_only": True}, "user": {"read_only": True}, 
                        "created_at": {"read_only": True}, "updated_at": {"read_only": True}}
        
    def create(self, validated_data):
        user = self.context.get('user')
        review = FacilityReview.objects.create(user=user, **validated_data)
        return review
    
    def get_user_name(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            user_name = f"{profile.first_name} {profile.last_name}"
            return user_name if user_name else None
        except Profile.DoesNotExist:
            return None
        
    def get_user_start(self, obj):
        return obj.user.date_joined
    
    def get_user_pfp(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.profile_pic.url if profile.profile_pic else None
        except Profile.DoesNotExist:
            return None
    
    def get_facility_name(self, obj):
        return obj.facility.name
    
class FacilityReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReview
        fields = ["id", "user", "booking", "facility", "rating", 
                  "content", "created_at", "updated_at"]
        extra_kwargs = {"id": {"read_only": True}, "user": {"read_only": True}, 
                        "booking": {"read_only": True}, "facility": {"read_only": True}, 
                        "created_at": {"read_only": True}, "updated_at": {"read_only": True}}