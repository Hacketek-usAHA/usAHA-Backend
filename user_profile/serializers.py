from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','first_name', 'last_name', 'bio', 'contact_number', 'profile_pic']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context.get('user')
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
    
    def update(self, instance, validated_data):
        validated_data.pop('profile_pic', None)
        return super().update(instance, validated_data)
    
class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic']
